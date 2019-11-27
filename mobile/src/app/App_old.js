import React,  {useState} from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect, withRouter } from "react-router-dom";

import AuthLayout from "layouts/Auth.js";
import RtlLayout from "layouts/RTL.js";
import AdminLayout from "layouts/Admin.js";

import "assets/scss/material-dashboard-pro-react.scss?v=1.8.0";
import { createContext, useContext } from 'react';

//import AuthContext from './context/auth';
import PrivateRoute from './PrivateRoute';



export default function App(props) {

    const hist = createBrowserHistory();
    const [authTokens, setAuthTokens] = useState();
    /*
    const setTokens = (data) => {
      localStorage.setItem("tokens", JSON.stringify(data));
      setAuthTokens(data);
    }
    */
    const AuthContext = createContext();
    const token = localStorage.getItem('token');
    console.log("App içinden token:"+token);

    return (
        <AuthContext.Provider value={token}>
            <Router history={hist}>
                <Switch>
                    <PrivateRoute path="/rtl" component={RtlLayout} />
                    <PrivateRoute path="/auth" component={AuthLayout} />
                    <PrivateRoute path="/admin" component={AdminLayout} />
                    <Redirect from="/" to="/admin/dashboard" />  
      
                </Switch>
            </Router>
        </AuthContext.Provider>    
    )
}

