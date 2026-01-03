class NotificationService {
  constructor() {
    this.isSupported = 'serviceWorker' in navigator && 'PushManager' in window;
  }

  // Check if browser supports notifications
  isNotificationSupported() {
    return 'Notification' in window;
  }

  // Request notification permission
  async requestPermission() {
    if (!this.isNotificationSupported()) {
      console.warn('Notifications are not supported in this browser');
      return 'unsupported';
    }

    if (Notification.permission === 'granted') {
      return 'granted';
    }

    const permission = await Notification.requestPermission();
    return permission;
  }

  // Show a notification
  showNotification(title, options = {}) {
    if (!this.isNotificationSupported()) {
      console.warn('Notifications are not supported in this browser');
      return Promise.reject(new Error('Notifications not supported'));
    }

    if (Notification.permission !== 'granted') {
      return Promise.reject(new Error('Notification permission not granted'));
    }

    return new Promise((resolve, reject) => {
      try {
        const notification = new Notification(title, options);
        notification.onclick = () => {
          // Handle notification click
          window.focus();
        };
        notification.onerror = reject;
        notification.onshow = resolve;
      } catch (error) {
        reject(error);
      }
    });
  }

  // Register service worker for push notifications
  async registerServiceWorker() {
    if (!this.isSupported) {
      console.warn('Push notifications are not supported in this browser');
      return null;
    }

    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      console.log('Service Worker registered with scope:', registration.scope);
      return registration;
    } catch (error) {
      console.error('Service Worker registration failed:', error);
      throw error;
    }
  }

  // Subscribe to push notifications
  async subscribeToPush(registration, publicKey) {
    if (!this.isSupported) {
      throw new Error('Push notifications are not supported in this browser');
    }

    try {
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: publicKey,
      });

      return subscription;
    } catch (error) {
      console.error('Push subscription failed:', error);
      throw error;
    }
  }

  // Unsubscribe from push notifications
  async unsubscribeFromPush(registration) {
    try {
      const subscription = await registration.pushManager.getSubscription();
      if (subscription) {
        await subscription.unsubscribe();
        console.log('Unsubscribed from push notifications');
        return true;
      }
      return false;
    } catch (error) {
      console.error('Unsubscribe failed:', error);
      return false;
    }
  }

  // Send notification data to backend
  async sendSubscriptionToBackend(subscription, userId) {
    try {
      const response = await fetch('/api/v1/notifications/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          subscription: subscription,
          user_id: userId,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send subscription to backend');
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending subscription to backend:', error);
      throw error;
    }
  }
}

export default new NotificationService();