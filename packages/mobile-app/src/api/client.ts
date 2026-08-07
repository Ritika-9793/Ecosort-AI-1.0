import axios from 'axios';

export const apiClient = axios.create({
  baseURL: 'http://10.0.2.2:8000/api/v1', // 10.0.2.2 points to host machine from Android Emulator
  headers: {
    'Content-Type': 'application/json'
  }
});
