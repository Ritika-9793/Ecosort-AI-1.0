import React from 'react';
import { SafeAreaView, StatusBar, StyleSheet } from 'react-native';
import { useAuthStore } from './state/authStore';
import { LoginScreen } from './screens/LoginScreen';
import { HomeScreen } from './screens/HomeScreen';
import './localization/i18n';

export const App = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#090D16" />
      {isAuthenticated ? <HomeScreen /> : <LoginScreen />}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#090D16',
  },
});

export default App;
