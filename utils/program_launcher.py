import os
import subprocess
from rapidfuzz import process, fuzz
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ProgramLauncher:
    def __init__(self):
        self.programs = self._scan_programs()
    
    def _scan_programs(self):
        """Scan for installed programs"""
        programs = {}
        
        search_paths = [
            os.path.join(
                os.environ.get("APPDATA", ""),
                r"Microsoft\Windows\Start Menu\Programs"
            ),
            os.path.join(
                os.environ.get("PROGRAMDATA", ""),
                r"Microsoft\Windows\Start Menu\Programs"
            ),
            os.path.join(
                os.environ.get("USERPROFILE", ""),
                "Desktop"
            ),
            os.path.join(
                os.environ.get("PROGRAMFILES", ""),
            ),
        ]
        
        for base in search_paths:
            if not os.path.exists(base):
                continue
            
            try:
                for root, dirs, files in os.walk(base):
                    for file in files:
                        if file.endswith((".lnk", ".exe")):
                            name = os.path.splitext(file)[0].lower()
                            programs[name] = os.path.join(root, file)
            except Exception as e:
                logger.debug(f"Error scanning {base}: {e}")
        
        logger.info(f"Found {len(programs)} programs")
        return programs
    
    def open(self, program_name):
        """Open a program by name"""
        if not program_name:
            return
        
        # Fuzzy match
        result = process.extractOne(
            program_name.lower(),
            self.programs.keys(),
            scorer=fuzz.WRatio
        )
        
        if not result:
            logger.warning(f"Program not found: {program_name}")
            return
        
        best_match, score, _ = result
        
        if score < 60:
            logger.warning(f"Low match score for {program_name}: {score}")
            return
        
        filepath = self.programs[best_match]
        
        try:
            logger.info(f"Opening: {best_match} ({filepath})")
            os.startfile(filepath)
        except Exception as e:
            logger.error(f"Error opening program: {e}")
            try:
                subprocess.Popen(["cmd", "/c", "start", "", filepath], shell=True)
            except Exception as e2:
                logger.error(f"Fallback failed: {e2}")