import React from "react";
import { Route, Redirect, Link } from "react-router-dom";



function PrivateRoute({ component: Component, ...rest })  {
  
  const authTokens = localStorage.getItem('token');
  console.log({...rest});
  console.log({Component});

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

