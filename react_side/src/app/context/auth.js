import { createContext, useContext } from 'react';

const AuthContext = createContext();

export default function useAuth() {
  return useContext(AuthContext);
}

