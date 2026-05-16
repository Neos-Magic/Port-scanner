"""
Network Port Scanner Tool
Escanea puertos en máquinas locales y remotas
"""

import socket
import json
import threading
from datetime import datetime
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, asdict
import ipaddress


@dataclass
class ScanResult:
    """Estructura para almacenar resultados del escaneo"""
    ip: str
    port: int
    state: str  # 'open', 'closed', 'filtered'
    service: str
    timestamp: str


class PortScanner:
    """Herramienta para escanear puertos en la red"""
    
    # Servicios comunes por puerto
    COMMON_SERVICES = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt',
        9200: 'Elasticsearch',
        27017: 'MongoDB',
    }
    
    def __init__(self, timeout: float = 2.0, threads: int = 100):
        """
        Inicializa el scanner
        
        Args:
            timeout: Tiempo de espera en segundos para cada conexión
            threads: Número de threads para escaneo paralelo
        """
        self.timeout = timeout
        self.threads = threads
        self.results: List[ScanResult] = []
        self.lock = threading.Lock()
    
    def _get_service_name(self, port: int) -> str:
        """Obtiene el nombre del servicio conocido para un puerto"""
        return self.COMMON_SERVICES.get(port, 'Unknown')
    
    def _scan_port(self, ip: str, port: int) -> Tuple[str, int, str]:
        """
        Escanea un puerto específico
        
        Args:
            ip: Dirección IP a escanear
            port: Número de puerto
            
        Returns:
            Tupla (ip, port, estado)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                return ip, port, 'open'
            else:
                return ip, port, 'closed'
        except socket.gaierror:
            return ip, port, 'error'
        except socket.timeout:
            return ip, port, 'filtered'
        except Exception as e:
            return ip, port, 'error'
    
    def scan_single_ip(self, ip: str, ports: List[int] = None) -> List[ScanResult]:
        """
        Escanea una sola dirección IP
        
        Args:
            ip: Dirección IP a escanear
            ports: Lista de puertos (None para puertos comunes)
            
        Returns:
            Lista de resultados del escaneo
        """
        if ports is None:
            ports = list(self.COMMON_SERVICES.keys())
        
        self.results = []
        threads_list = []
        
        print(f"\n[*] Escaneando IP: {ip}")
        print(f"[*] Puertos a escanear: {len(ports)}")
        print(f"[*] Usando {self.threads} threads\n")
        
        # Crear y ejecutar threads
        for port in ports:
            thread = threading.Thread(target=self._scan_port_threaded, args=(ip, port))
            threads_list.append(thread)
            thread.start()
            
            # Limitar cantidad de threads activos
            if len([t for t in threads_list if t.is_alive()]) >= self.threads:
                for t in threads_list:
                    t.join()
                threads_list = [t for t in threads_list if t.is_alive()]
        
        # Esperar a que terminen todos los threads
        for thread in threads_list:
            thread.join()
        
        # Ordenar resultados por puerto
        self.results.sort(key=lambda x: x.port)
        return self.results
    
    def _scan_port_threaded(self, ip: str, port: int):
        """Versión threaded de scan_port"""
        ip_result, port_result, state = self._scan_port(ip, port)
        
        if state == 'open':
            service = self._get_service_name(port)
            result = ScanResult(
                ip=ip_result,
                port=port_result,
                state=state,
                service=service,
                timestamp=datetime.now().isoformat()
            )
            
            with self.lock:
                self.results.append(result)
                print(f"[+] {ip}:{port} - {state.upper()} ({service})")
    
    def scan_network(self, network: str, ports: List[int] = None) -> List[ScanResult]:
        """
        Escanea una red completa (ej: 192.168.1.0/24)
        
        Args:
            network: Red en formato CIDR
            ports: Lista de puertos
            
        Returns:
            Lista de resultados del escaneo
        """
        if ports is None:
            ports = list(self.COMMON_SERVICES.keys())
        
        try:
            net = ipaddress.ip_network(network, strict=False)
            ips = [str(ip) for ip in net.hosts()]
        except ValueError:
            print(f"[-] Red inválida: {network}")
            return []
        
        print(f"\n[*] Escaneando red: {network}")
        print(f"[*] Hosts a escanear: {len(ips)}")
        print(f"[*] Puertos por host: {len(ports)}\n")
        
        all_results = []
        threads_list = []
        
        for ip in ips:
            thread = threading.Thread(target=self._scan_ip_in_network, args=(ip, ports, all_results))
            threads_list.append(thread)
            thread.start()
            
            # Limitar threads activos
            if len([t for t in threads_list if t.is_alive()]) >= self.threads:
                for t in threads_list:
                    t.join()
                threads_list = [t for t in threads_list if t.is_alive()]
        
        for thread in threads_list:
            thread.join()
        
        all_results.sort(key=lambda x: (x.ip, x.port))
        self.results = all_results
        return self.results
    
    def _scan_ip_in_network(self, ip: str, ports: List[int], results: list):
        """Escanea una IP dentro de una red"""
        for port in ports:
            ip_result, port_result, state = self._scan_port(ip, port)
            
            if state == 'open':
                service = self._get_service_name(port)
                result = ScanResult(
                    ip=ip_result,
                    port=port_result,
                    state=state,
                    service=service,
                    timestamp=datetime.now().isoformat()
                )
                results.append(result)
                print(f"[+] {ip}:{port} - OPEN ({service})")
    
    def export_results(self, filename: str, format: str = 'json') -> bool:
        """
        Exporta resultados a un archivo
        
        Args:
            filename: Nombre del archivo
            format: Formato de salida ('json' o 'csv')
            
        Returns:
            True si fue exitoso, False en caso contrario
        """
        try:
            if format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump([asdict(r) for r in self.results], f, indent=2, ensure_ascii=False)
            
            elif format == 'csv':
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['IP', 'Puerto', 'Estado', 'Servicio', 'Fecha'])
                    for result in self.results:
                        writer.writerow([result.ip, result.port, result.state, result.service, result.timestamp])
            
            print(f"\n[+] Resultados exportados a: {filename}")
            return True
        
        except Exception as e:
            print(f"[-] Error al exportar: {e}")
            return False
    
    def print_summary(self):
        """Imprime un resumen de los resultados"""
        if not self.results:
            print("\n[!] No se encontraron puertos abiertos")
            return
        
        open_ports = [r for r in self.results if r.state == 'open']
        
        print("\n" + "="*60)
        print("RESUMEN DEL ESCANEO")
        print("="*60)
        print(f"Total de puertos escaneados: {len(self.results)}")
        print(f"Puertos abiertos: {len(open_ports)}")
        print(f"Fecha del escaneo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nPUERTOS ABIERTOS:")
        print("-" * 60)
        
        for result in open_ports:
            print(f"  {result.ip}:{result.port:<5} - {result.service:<15} - {result.state}")
        
        print("="*60)
