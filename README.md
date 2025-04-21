# Windows UAC Prompt Clone

## ⚠️ Educational Purposes Only

This tool is designed for **educational red team exercises** and **security awareness training** only. Unauthorized use against systems without explicit permission is illegal and unethical.

## Overview

This application creates a pixel-perfect clone of the Windows User Account Control (UAC) prompt that can be customized and deployed in security assessments. When users enter credentials and click "Yes," the information is sent to a Discord webhook for collection and analysis.

![UAC Prompt Clone](/Windows-UAC-Prompt.png)


## 🔍 Features

- **Visual Accuracy**: Meticulously styled to match the authentic Windows UAC prompt
- **Credential Harvesting**: Captures entered credentials and sends them via Discord webhook
- **Customization**: Easily modify the application name, publisher, and icon
- **Stealth Operation**: Minimizes user suspicion with authentic behavior
- **Cross-Platform Development**: Built with Electron for easy modification
- **Executable Building**: Package as a standalone Windows executable

## 📋 Requirements

- **Node.js**: v14.0.0 or higher
- **Electron**: v35.0.0 or higher
- **Python 3.x**: For customization script
- **Discord Webhook**: For receiving captured credentials

## 🔧 Quick Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/uac-prompt-clone.git
   cd uac-prompt-clone
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the customization script:
   ```
   python uac.py
   ```

4. Enter your customization options when prompted:
   - Application name (e.g., "Printer driver software installation")
   - Publisher name (e.g., "Microsoft Windows")
   - Discord webhook URL
   - Custom icon path (optional)

5. Choose whether to build the executable or run directly

## 🚀 Manual Operation

### Running with Electron
```
npx electron .
```

### Building the Executable
```
npm install --save-dev electron-builder
npm run build
```

The executable will be created in the `dist` directory.

## 📝 Customization

The UAC Prompt Clone can be customized using the included Python script:

### Using the Customization Script
```
python uac.py
```

### Available Customization Options:
- **Application Name**: The name displayed in the UAC dialog
- **Publisher Name**: The verified publisher name shown in the dialog
- **Discord Webhook URL**: Where captured credentials will be sent
- **Custom Icon**: Replace the default icon with your own (SVG, PNG, JPG supported)

## 📡 Discord Webhook Setup

1. Create a Discord server or use an existing one
2. Create a channel for receiving credentials
3. Channel Settings → Integrations → Webhooks → New Webhook
4. Copy the webhook URL and use it in the customization script

## 🧰 Technical Details

### Project Structure
- `index.js`: Main Electron process
- `index.html`: UAC dialog interface
- `styles.css`: Visual styling for authentic appearance
- `renderer.js`: UI interaction handling
- `preload.js`: Security bridge for Electron
- `uac.py`: Customization and build script

### Technology Stack
- **Electron**: Application framework
- **HTML/CSS/JavaScript**: User interface
- **Python**: Customization automation
- **Node.js**: Runtime environment
- **electron-builder**: Packaging and distribution

## ⚙️ Advanced Configuration

### Package.json Configuration
The build configuration in `package.json` can be modified for more advanced packaging options:

```json
"build": {
  "appId": "com.uac.prompt.clone",
  "productName": "UAC Prompt",
  "directories": {
    "output": "dist"
  },
  "win": {
    "target": "portable",
    "icon": "assets/icon.png"
  }
}
```

### Custom Icons
For the best results with custom icons:
- Use PNG format for electron-builder
- SVG format works best for the application UI
- Recommended size: 256x256 pixels

## 📚 Red Team Usage Notes

### Deployment Scenarios
- Phishing campaigns
- Social engineering assessments
- Security awareness training
- Endpoint security testing

### Operational Security
- Test in isolated environments first
- Keep logs of all deployments for security audits
- Inform leadership before deployment in production

### Effectiveness Metrics
- Credential capture rate
- Time to user interaction
- Suspicion indicators from targets

## 🛡️ Defending Against Similar Attacks

### For Security Teams
- Train users to recognize authentic system dialogs
- Implement strong application control policies
- Deploy behavioral analysis tools that can detect spoofed system dialogs
- Configure Windows to use personalized UAC prompts where possible


## 🤝 Disclaimer

This tool is developed for educational purposes and authorized red team security assessments only. The developers assume no liability for misuse or damage caused by this tool. Always obtain proper authorization before security testing.

---

*Remember: With great power comes great responsibility. Use this tool ethically and legally.*
