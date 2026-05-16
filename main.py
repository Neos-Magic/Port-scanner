#!/usr/bin/env python3
"""
CLI para Network Port Scanner
Interfaz de línea de comandos para escanear puertos
"""

import argparse
import sys
from port_scanner import PortScanner


def parse_ports(port_string: str) -> list:
    """
    Parsea un string de puertos
    Formatos: "22,80,443" o "1-100" o "common" (para puertos comunes)
    """
    if port_string.lower() == 'common':
        return list(PortScanner.COMMON_SERVICES.keys())
    
    ports = []
    parts = port_string.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            except ValueError:
                print(f"[-] Formato de rango inválido: {part}")
                sys.exit(1)
        else:
            try:
                ports.append(int(part))
            except ValueError:
                print(f"[-] Puerto inválido: {part}")
                sys.exit(1)
    
    return sorted(list(set(ports)))


def main():
    parser = argparse.ArgumentParser(
        description='🔍 Network Port Scanner - Escanea puertos en tu red',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Escanear una IP con puertos comunes
  python main.py -i 192.168.1.100
  
  # Escanear una IP con puertos específicos
  python main.py -i 192.168.1.100 -p 22,80,443,3306
  
  # Escanear un rango de puertos
  python main.py -i 192.168.1.100 -p 1-1000
  
  # Escanear una red completa
  python main.py -n 192.168.1.0/24 -p common
  
  # Escanear y exportar resultados
  python main.py -i 192.168.1.100 -e resultados.json
        """
    )
    
    parser.add_argument('-i', '--ip', type=str, help='IP a escanear')
    parser.add_argument('-n', '--network', type=str, help='Red a escanear (ej: 192.168.1.0/24)')
    parser.add_argument('-p', '--ports', type=str, default='common',
                       help='Puertos: "common", "1-1000", o "22,80,443" (default: common)')
    parser.add_argument('-t', '--timeout', type=float, default=2.0,
                       help='Timeout para conexiones en segundos (default: 2.0)')
    parser.add_argument('--threads', type=int, default=100,
                       help='Número de threads paralelos (default: 100)')
    parser.add_argument('-e', '--export', type=str, help='Exportar resultados (archivo: formato.json o formato.csv)')
    parser.add_argument('-f', '--format', type=str, choices=['json', 'csv'], default='json',
                       help='Formato de exportación (default: json)')
    
    args = parser.parse_args()
    
    # Validar que se proporcionó IP o red
    if not args.ip and not args.network:
        print("[-] Error: Debes especificar -i (IP) o -n (red)")
        print("Usa -h para ver más ayuda")
        sys.exit(1)
    
    # Parsear puertos
    ports = parse_ports(args.ports)
    
    # Limitar puertos a máximo 65535
    ports = [p for p in ports if 1 <= p <= 65535]
    
    if not ports:
        print("[-] Error: No se especificaron puertos válidos")
        sys.exit(1)
    
    # Crear scanner
    scanner = PortScanner(timeout=args.timeout, threads=args.threads)
    
    try:
        # Ejecutar escaneo
        if args.ip:
            results = scanner.scan_single_ip(args.ip, ports)
        else:
            results = scanner.scan_network(args.network, ports)
        
        # Mostrar resumen
        scanner.print_summary()
        
        # Exportar si se solicitó
        if args.export:
            # Determinar formato si no es explícito
            if not args.export.endswith(('.json', '.csv')):
                args.export += f'.{args.format}'
            
            scanner.export_results(args.export, args.format)
    
    except KeyboardInterrupt:
        print("\n\n[-] Escaneo cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error durante el escaneo: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
