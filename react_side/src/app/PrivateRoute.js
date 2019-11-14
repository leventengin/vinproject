import React from "react";
import { Route, Redirect, Link } from "react-router-dom";
import { useAuth } from "./context/auth";
import { createContext, useContext } from 'react';
import AuthContext from "./App";


function PrivateRoute({ component: Component, ...rest })  {
  //const { authTokens } = useAuth();
  const authTokens = localStorage.getItem('token');

  console.log("private_route...auth_tokens:"+authTokens);

  return (
    <Route
      {...rest}
      render={props =>
        authTokens ? (
          <Component {...props} />
        ) : (
          <Redirect to="/auth/login-page"  />
        )
      }
    />
  );
}

export default PrivateRoute;

