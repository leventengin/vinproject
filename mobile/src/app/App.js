import React,  {useState, useEffect} from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect, withRouter } from "react-router-dom";

import AuthLayout from "layouts/Auth.js";
import RtlLayout from "layouts/RTL.js";
import AdminLayout from "layouts/Admin.js";

import "assets/scss/material-dashboard-pro-react.scss?v=1.8.0";
import { createContext, useContext } from 'react';
import io from 'socket.io-client/dist/socket.io';

import PrivateRoute from './PrivateRoute';



export default function App() {

    const hist = createBrowserHistory();

    function wait(ms){
      var start = new Date().getTime();
      var end = start;
      while(end < start + ms) {
        end = new Date().getTime();
        console.log(end);

      };
    };

    function gonder(){
      var msg = {
          type: "send_location",
          latitude: "12.4455666",
          longtitude:"45.3322222",
          rid:"2"
        };

       if (ws.readyState === WebSocket.OPEN) {
           ws.send(JSON.stringify(msg));
       }
    }





    const path = `ws://127.0.0.1:8000/kurye`;
    const ws = new WebSocket(path);
    console.log("state of ws-1 ");
    console.log(ws.readyState);

    //wait(5000);

    console.log("state of ws-2 ");
    console.log(ws.readyState);

    ws.onopen = () => {
     console.log("WebSocket now open...");
     console.log(ws.readyState);
     gonder();
    };


    console.log("state of ws-3");
    console.log(ws.readyState);




    ws.onclose = () => {
          console.log("WebSocket now closed...");
          console.log(ws.readyState);
    };








    const AuthContext = createContext();
    const token = localStorage.getItem('token');
    console.log("App içinden token:"+token);




    return (
        <AuthContext.Provider value={token}>
            <Router history={hist}>
                <Switch>
                    { (token == "") && <Route path="/auth" component={AuthLayout} />}
                    <Route path="/rtl" component={RtlLayout} />
                    <Route path="/auth" component={AuthLayout} />
                    <Route path="/admin" component={AdminLayout} />
                    <Redirect from="/" to="/admin/dashboard" />
                </Switch>
            </Router>
        </AuthContext.Provider>
    )
}
