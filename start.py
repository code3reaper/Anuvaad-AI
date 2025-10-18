#!/usr/bin/env python3
"""
Anuvaad AI Startup Script
Starts both backend and frontend servers with a single command
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path
import shutil

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("\n📝 Please create a .env file with your API keys.")
        print("   You can copy .env.example and fill in your keys:")
        print("   cp .env.example .env")
        print("\n   Then edit .env and add your API keys.")
        sys.exit(1)
    print("✅ .env file found")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    # Check Node.js
    try:
        subprocess.run(['node', '--version'], check=True, capture_output=True)
        print("✅ Node.js is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is not installed. Please install it from https://nodejs.org/")
        sys.exit(1)
    # Check npm presence (on Windows npm may be available as npm.cmd)
    # expose npm executable path for other functions
    npm_exec = shutil.which('npm') or shutil.which('npm.cmd')
    global NPM_EXEC
    NPM_EXEC = npm_exec
    if not npm_exec:
        print("\n❌ npm was not found on your PATH. Node.js may be installed but npm is missing.")
        print("   Install Node.js from https://nodejs.org/ or ensure npm is on your PATH.")
        print("   You can check by running: npm --version")
        sys.exit(1)

    # Check if frontend dependencies are installed
    if not os.path.exists('frontend/node_modules'):
        print("\n📦 Installing frontend dependencies...")
        try:
            subprocess.run([npm_exec, 'install'], cwd='frontend', check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            sys.exit(1)
    else:
        print("✅ Frontend dependencies are installed")

def start_servers():
    """Start both backend and frontend servers"""
    processes = []
    
    try:
        print("\n" + "="*60)
        print("🚀 Starting Anuvaad AI...")
        print("="*60)
        
        # Start backend
        print("\n📡 Starting Backend Server (Flask)...")
        backend_process = subprocess.Popen(
            [sys.executable, 'backend.py']
        )
        processes.append(('backend', backend_process))
        # Give backend time to start and read the actual port from backend_port.txt
        time.sleep(1)
        backend_port = 5001
        for _ in range(10):
            try:
                with open('backend_port.txt', 'r') as f:
                    backend_port = int(f.read().strip())
                    break
            except Exception:
                time.sleep(0.5)

        print(f"✅ Backend started on http://localhost:{backend_port}")
        
        # Start frontend
        print("\n🎨 Starting Frontend Server (Vite)...")
        frontend_cmd = [NPM_EXEC, 'run', 'dev', '--', '--host', '0.0.0.0', '--port', '5000']
        frontend_process = subprocess.Popen(
            frontend_cmd,
            cwd='frontend'
        )
        processes.append(('frontend', frontend_process))
        time.sleep(3)  # Give frontend time to start
        
        print("\n" + "="*60)
        print("✅ Anuvaad AI is now running!")
        print("="*60)
        print("\n🌐 Open your browser and go to:")
        print("   👉 http://localhost:5000")
        print("\n📊 Backend API running at:")
        print(f"   👉 http://localhost:{backend_port}")
        print("\n⏹️  Press Ctrl+C to stop both servers")
        print("="*60 + "\n")
        
        # Keep the script running and show output
        while True:
            time.sleep(1)
            
            # Check if any process has died
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"\n❌ A server process ('{name}') stopped unexpectedly with exit code {proc.returncode}")
                    raise KeyboardInterrupt
                    
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping servers...")
        for name, proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
        print("✅ All servers stopped")
        print("\nThank you for using Anuvaad AI! 👋\n")
        sys.exit(0)

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🎬 ANUVAAD AI STARTUP SCRIPT 🎬             ║
    ║                                                           ║
    ║           AI-Powered Video Dubbing Platform               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    check_env_file()
    check_dependencies()
    start_servers()
