import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Colors } from '../theme/colors';
import { useAuthStore } from '../state/authStore';

export const HomeScreen = () => {
  const { user, logout } = useAuthStore();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, {user?.full_name}!</Text>
      <Text style={styles.subtitle}>Role: {user?.role}</Text>

      <View style={styles.card}>
        <Text style={styles.cardLabel}>Eco-Coins Balance</Text>
        <Text style={styles.cardValue}>{user?.rewards_balance ?? 0} PTS</Text>
      </View>

      <TouchableOpacity style={styles.logoutButton} onPress={logout}>
        <Text style={styles.logoutText}>Log Out</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    padding: 24,
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: Colors.textPrimary,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 14,
    color: Colors.primary,
    textAlign: 'center',
    marginBottom: 24,
  },
  card: {
    backgroundColor: Colors.cardBg,
    borderColor: Colors.cardBorder,
    borderWidth: 1,
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginBottom: 32,
  },
  cardLabel: {
    color: Colors.textSecondary,
    fontSize: 12,
    textTransform: 'uppercase',
  },
  cardValue: {
    color: Colors.textPrimary,
    fontSize: 32,
    fontWeight: 'bold',
    marginTop: 8,
  },
  logoutButton: {
    backgroundColor: 'rgba(244, 63, 94, 0.15)',
    borderColor: Colors.error,
    borderWidth: 1,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  logoutText: {
    color: Colors.error,
    fontWeight: 'bold',
  },
});
