"""
Dependency pre-check to ensure all required packages are installed.
This prevents runtime downloads during server initialization that cause timeouts.
"""

import sys
import subprocess
import platform
import logging
import os
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

def check_torch_installed() -> Tuple[bool, Optional[str]]:
    """
    Check if PyTorch is properly installed.
    Returns (is_installed, version_string)
    """
    try:
        import torch
        # Check if torch has __version__ attribute (it should)
        version = getattr(torch, '__version__', 'unknown')
        # Also verify torch is functional
        try:
            _ = torch.tensor([1.0])
            return True, version
        except Exception:
            return False, None
    except ImportError:
        return False, None

def check_sentence_transformers_installed() -> Tuple[bool, Optional[str]]:
    """
    Check if sentence-transformers is properly installed.
    Returns (is_installed, version_string)
    """
    try:
        import sentence_transformers
        return True, sentence_transformers.__version__
    except ImportError:
        return False, None

def check_critical_dependencies() -> Tuple[bool, list]:
    """
    Check if all critical dependencies are installed.
    Returns (all_installed, missing_packages)
    """
    missing = []
    
    # Check PyTorch
    torch_installed, torch_version = check_torch_installed()
    if not torch_installed:
        missing.append("torch")
    else:
        logger.debug(f"PyTorch {torch_version} is installed")
    
    # Check sentence-transformers
    st_installed, st_version = check_sentence_transformers_installed()
    if not st_installed:
        missing.append("sentence-transformers")
    else:
        logger.debug(f"sentence-transformers {st_version} is installed")
    
    # Check other critical packages
    critical_packages = [
        "chromadb",
        "sqlite-vec",
        "mcp",
        "aiohttp",
        "fastapi",
        "uvicorn"
    ]
    
    for package in critical_packages:
        try:
            __import__(package.replace("-", "_"))
            logger.debug(f"{package} is installed")
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0, missing

def suggest_installation_command(missing_packages: list) -> str:
    """
    Generate the appropriate installation command for missing packages.
    """
    if not missing_packages:
        return ""
    
    # For Windows, suggest running install.py
    if platform.system() == "Windows":
        return "python install.py"
    else:
        return "python install.py"

def run_dependency_check() -> bool:
    """
    Run the dependency check and provide user feedback.
    Returns True if all dependencies are satisfied, False otherwise.
    """
    print("\n=== MCP Memory Service Dependency Check ===", file=sys.stderr, flush=True)
    
    all_installed, missing = check_critical_dependencies()
    
    if all_installed:
        print("✅ All dependencies are installed", file=sys.stderr, flush=True)
        return True
    else:
        print(f"❌ Missing dependencies detected: {', '.join(missing)}", file=sys.stderr, flush=True)
        print("\n⚠️  IMPORTANT: Missing dependencies will cause timeouts!", file=sys.stderr, flush=True)
        print("📦 To install missing dependencies, run:", file=sys.stderr, flush=True)
        print(f"   {suggest_installation_command(missing)}", file=sys.stderr, flush=True)
        print("\nThe server will attempt to continue, but may timeout during initialization.", file=sys.stderr, flush=True)
        print("============================================\n", file=sys.stderr, flush=True)
        
        # Don't block startup, but warn that it might fail
        return False

def is_first_run() -> bool:
    """
    Check if this appears to be the first run of the server.
    """
    # Check if model cache exists
    cache_indicators = [
        os.path.expanduser("~/.cache/torch/sentence_transformers"),
        os.path.expanduser("~/.cache/huggingface"),
        os.path.expanduser("~/AppData/Local/sentence-transformers"),  # Windows
    ]
    
    for path in cache_indicators:
        if os.path.exists(path) and os.listdir(path):
            return False
    
    return True

def get_recommended_timeout() -> float:
    """
    Get the recommended timeout based on system and dependencies.
    """
    # Check if dependencies are missing
    all_installed, missing = check_critical_dependencies()
    
    # Check if it's first run (models need downloading)
    first_run = is_first_run()
    
    # Base timeout
    timeout = 30.0 if platform.system() == "Windows" else 15.0
    
    # Extend timeout if dependencies are missing
    if not all_installed:
        timeout *= 2  # Double the timeout
        logger.warning(f"Dependencies missing, extending timeout to {timeout}s")
    
    # Extend timeout if it's first run
    if first_run:
        timeout *= 2  # Double the timeout
        logger.warning(f"First run detected, extending timeout to {timeout}s")
    
    return timeout