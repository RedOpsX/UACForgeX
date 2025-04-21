const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld(
  'api', {
    submitCredentials: (credentials) => {
      return ipcRenderer.invoke('submit-credentials', credentials);
    },
    closeApp: () => {
      ipcRenderer.send('close-app');
    }
  }
);
