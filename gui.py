#!/usr/bin/env python3
"""
GUI para Network Port Scanner
Interfaz gráfica multiplataforma (Windows, Linux, macOS)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from port_scanner import PortScanner
import sys


class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Network Port Scanner")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variable para controlar el escaneo
        self.scanning = False
        self.scanner = None
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
    
    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        
        # Colores
        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)
        
        style.theme_use('clam')
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color)
        style.configure('Header.TLabel', background=bg_color, font=('Arial', 12, 'bold'))
        style.configure('Title.TLabel', background=bg_color, font=('Arial', 14, 'bold'))
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="🔍 Scanner de Puertos de Red", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # ===== SECCIÓN DE ENTRADA =====
        input_frame = ttk.LabelFrame(main_frame, text="Configuración del Escaneo", padding="10")
        input_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Selección IP o Red
        ttk.Label(input_frame, text="Modo:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.mode_var = tk.StringVar(value="ip")
        ttk.Radiobutton(input_frame, text="Escanear IP Individual", variable=self.mode_var, 
                       value="ip", command=self.update_mode).grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(input_frame, text="Escanear Red Completa", variable=self.mode_var, 
                       value="network", command=self.update_mode).grid(row=0, column=2, sticky=tk.W)
        
        # Entrada de IP/Red
        ttk.Label(input_frame, text="Objetivo:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.target_entry = ttk.Entry(input_frame, width=40)
        self.target_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        self.target_entry.insert(0, "192.168.1.1")
        
        # Puertos
        ttk.Label(input_frame, text="Puertos:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.ports_var = tk.StringVar(value="common")
        ports_frame = ttk.Frame(input_frame)
        ports_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(ports_frame, text="Comunes (21,22,80,443...)", variable=self.ports_var, 
                       value="common").pack(anchor=tk.W)
        ttk.Radiobutton(ports_frame, text="Personalizado:", variable=self.ports_var, 
                       value="custom").pack(anchor=tk.W)
        
        self.custom_ports_entry = ttk.Entry(ports_frame, width=40)
        self.custom_ports_entry.pack(anchor=tk.W, pady=3)
        self.custom_ports_entry.insert(0, "22,80,443,3306,8080")
        
        # Opciones avanzadas
        ttk.Label(input_frame, text="Opciones Avanzadas:", style='Header.TLabel').grid(row=3, column=0, sticky=tk.W, pady=10)
        
        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Label(options_frame, text="Timeout (seg):").pack(side=tk.LEFT, padx=5)
        self.timeout_spin = ttk.Spinbox(options_frame, from_=0.5, to=10, width=5)
        self.timeout_spin.set(2.0)
        self.timeout_spin.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(options_frame, text="Threads:").pack(side=tk.LEFT, padx=5)
        self.threads_spin = ttk.Spinbox(options_frame, from_=10, to=500, width=5)
        self.threads_spin.set(100)
        self.threads_spin.pack(side=tk.LEFT, padx=5)
        
        # ===== BOTONES =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        self.scan_button = ttk.Button(button_frame, text="▶ Iniciar Escaneo", command=self.start_scan)
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹ Detener", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="📋 Limpiar", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Exportar Resultados", command=self.export_results).pack(side=tk.LEFT, padx=5)
        
        # ===== ÁREA DE SALIDA =====
        output_frame = ttk.LabelFrame(main_frame, text="Resultados del Escaneo", padding="10")
        output_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=20, width=100, 
                                                      wrap=tk.WORD, font=('Courier', 9))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo para escanear")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def update_mode(self):
        """Actualiza el placeholder según el modo seleccionado"""
        if self.mode_var.get() == "network":
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, "192.168.1.0/24")
        else:
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, "192.168.1.1")
    
    def log_output(self, message):
        """Agrega mensaje al área de salida"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def start_scan(self):
        """Inicia el escaneo en un thread separado"""
        target = self.target_entry.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Debes ingresar un objetivo (IP o red)")
            return
        
        # Parsear puertos
        if self.ports_var.get() == "common":
            ports = list(PortScanner.COMMON_SERVICES.keys())
        else:
            try:
                ports_str = self.custom_ports_entry.get().strip()
                ports = self.parse_ports(ports_str)
                if not ports:
                    messagebox.showerror("Error", "No se especificaron puertos válidos")
                    return
            except Exception as e:
                messagebox.showerror("Error", f"Error al parsear puertos: {e}")
                return
        
        # Obtener configuración
        try:
            timeout = float(self.timeout_spin.get())
            threads = int(self.threads_spin.get())
        except ValueError:
            messagebox.showerror("Error", "Timeout y Threads deben ser números")
            return
        
        # Limitar puertos
        ports = [p for p in ports if 1 <= p <= 65535]
        
        # Deshabilitar botón de escaneo
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.scanning = True
        
        # Ejecutar escaneo en thread separado
        thread = threading.Thread(target=self.run_scan, args=(target, ports, timeout, threads))
        thread.daemon = True
        thread.start()
    
    def run_scan(self, target, ports, timeout, threads):
        """Ejecuta el escaneo"""
        try:
            self.log_output(f"\n{'='*80}")
            self.log_output(f"INICIANDO ESCANEO")
            self.log_output(f"{'='*80}\n")
            self.status_var.set("Escaneando...")
            
            self.scanner = PortScanner(timeout=timeout, threads=threads)
            
            mode = self.mode_var.get()
            
            if mode == "ip":
                self.log_output(f"[*] Objetivo: {target}")
                self.log_output(f"[*] Puertos a escanear: {len(ports)}\n")
                results = self.scanner.scan_single_ip(target, ports)
            else:
                self.log_output(f"[*] Red: {target}")
                self.log_output(f"[*] Puertos por host: {len(ports)}\n")
                results = self.scanner.scan_network(target, ports)
            
            # Mostrar resultados
            self.log_output(f"\n{'='*80}")
            self.log_output("RESULTADOS")
            self.log_output(f"{'='*80}\n")
            
            open_ports = [r for r in results if r.state == 'open']
            
            if open_ports:
                self.log_output(f"✓ Se encontraron {len(open_ports)} puerto(s) abierto(s):\n")
                for result in open_ports:
                    self.log_output(f"  ✓ {result.ip}:{result.port:<5} - {result.service:<15} (ABIERTO)")
            else:
                self.log_output("[!] No se encontraron puertos abiertos")
            
            self.log_output(f"\n{'='*80}\n")
            self.status_var.set(f"Escaneo completado: {len(open_ports)} puerto(s) abierto(s)")
        
        except Exception as e:
            self.log_output(f"\n[-] Error: {e}\n")
            self.status_var.set(f"Error: {e}")
        
        finally:
            self.scan_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.scanning = False
    
    def stop_scan(self):
        """Detiene el escaneo"""
        self.scanning = False
        self.log_output("\n[!] Escaneo cancelado por el usuario\n")
        self.status_var.set("Escaneo cancelado")
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def parse_ports(self, port_string):
        """Parsea puertos desde un string"""
        ports = []
        parts = port_string.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))
        
        return sorted(list(set(ports)))
    
    def clear_output(self):
        """Limpia el área de salida"""
        self.output_text.delete('1.0', tk.END)
        self.status_var.set("Área de salida limpiada")
    
    def export_results(self):
        """Exporta los resultados"""
        if not self.scanner or not self.scanner.results:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar. Realiza un escaneo primero.")
            return
        
        try:
            filename = "resultados_escaneo.json"
            self.scanner.export_results(filename, 'json')
            messagebox.showinfo("Éxito", f"Resultados exportados a: {filename}")
            self.log_output(f"\n[+] Resultados exportados a: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")


def main():
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
