import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API Service Methods
export const apiServices = {
  // Waste AI
  classifyWaste: (formData: FormData) => apiClient.post('/waste/classify', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  getScanHistory: () => apiClient.get('/waste/history'),

  // Centers & Pickups
  getNearbyCenters: (lat = 28.6139, lng = 77.2090) => apiClient.get(`/centers/nearby?lat=${lat}&lng=${lng}`),
  getCenterQR: (centerId: string) => apiClient.get(`/centers/${centerId}/qr`),
  schedulePickup: (data: any) => apiClient.post('/pickups/schedule', data),
  getMyPickups: () => apiClient.get('/pickups/my-pickups'),

  // Rewards & Badges
  getBadges: () => apiClient.get('/rewards/badges'),
  getLeaderboard: () => apiClient.get('/rewards/leaderboard'),

  // Notifications
  getNotifications: () => apiClient.get('/notifications'),
  markNotificationRead: (id: string) => apiClient.patch(`/notifications/${id}/read`),

  // Admin & Municipality
  getAdminAnalytics: () => apiClient.get('/admin/analytics'),
  getAdminUsers: () => apiClient.get('/admin/users'),
  getAuditLogs: () => apiClient.get('/admin/audit-logs'),
  getWardStats: () => apiClient.get('/municipality/ward-stats'),
  getHeatmapPoints: () => apiClient.get('/municipality/heatmap')
};
