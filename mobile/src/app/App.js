import React,  {useState, useEffect} from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect, withRouter } from "react-router-dom";
import axios from 'axios';

import AuthLayout from "layouts/Auth.js";
import RtlLayout from "layouts/RTL.js";
import AdminLayout from "layouts/Admin.js";

import "assets/scss/material-dashboard-pro-react.scss?v=1.8.0";
import { createContext, useContext } from 'react';
import io from 'socket.io-client/dist/socket.io';
import {API_BASE_URL, WS_BASE_URL} from "assets/jss/material-dashboard-pro-react";

import PrivateRoute from './PrivateRoute';



export default function App() {

      const hist = createBrowserHistory();

      function gonder(i){
          let y = i*0.001;
          // Göztepe parkı
          //var lat = 40.970894;
          //var lon = 29.056185;
          // CKM
          var lat = 40.998820;
          var lon = 29.087562;
          var lat_new = lat + y;
          var lon_new = lon + y;
          var msg = {
              type: "send_location",
              latitude: lat,
              longitude:lon,
            };
            console.log(i)
           if (ws.readyState === WebSocket.OPEN) {
               ws.send(JSON.stringify(msg));
           }
        }


      async function retrieveToken(token) {
        try{
              const urlx = `${API_BASE_URL}api/refresh`;
              console.log(token);
              console.log(urlx);
              //console.log(header)
              var result = await axios({
                  method: 'post',
                  url: urlx,
                  data: { "refresh": token },
                  headers:{
                      'Content-Type': 'application/json',
                      //'Accept': 'application/json',
                      //'Authorization': 'Bearer ' + token,
                    }
                  //headers: header,
                  });
              console.log(result);
              //setNewToken(result.data);
              //return;
          }
            catch (err) {
                console.log("----");
                console.log(err);
                //return;
            };
        };





      const AuthContext = createContext();

      var navigator_info = window.navigator;
      var screen_info = window.screen;
      console.log(navigator_info);
      console.log(screen_info);

      var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      };

      function success(pos) {
        var crd = pos.coords;
        console.log('Your current position is:');
        console.log(`Latitude : ${crd.latitude}`);
        console.log(`Longitude: ${crd.longitude}`);
        console.log(`More or less ${crd.accuracy} meters.`);
      }

      function error(err) {
        console.warn(`ERROR(${err.code}): ${err.message}`);
      }
      /*
      async function get_geo(){
        await navigator.geolocation.getCurrentPosition(success, error, options);
      }

      const geo = navigator.geolocation;
      if (!geo) {
        console.log("Geolocation is not supported");
      } else {
        console.log("yes geolocation");
        //get_geo();
      }
      */
      const newToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwODkwMTUzNSwianRpIjoiMzQwMWViNWE0OTgzNGNkNjkzNjEzNWY4Mzk4MzA0MDUiLCJ1c2VyX2lkIjoyfQ.WI-uD5YM0knA_JE_rTFBb7OgNN2XmA8HiTo1kYxI6is";
      //let newToken = retrieveToken(token)
      //const newToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc0OTQ3NzkxLCJqdGkiOiIwNWM4MjhjZTUzMjY0YmRhYjY5YWIxYjJmNmNmZDMxMiIsInVzZXJfaWQiOjJ9.dtFi9MB71ug3OvUb04NTA6GFQPnjVuRSkSFovsqNLSU";
      console.log(newToken);
      let endpoint = `${WS_BASE_URL}kurye/`
      //let endpoint = "ws://127.0.0.1:8000/kurye/"
      // Create new WebSocket
      let ws = new WebSocket(endpoint + "?token=" + newToken)

      console.log("state of ws-1 ");
      console.log(ws.readyState);

      ws.onmessage = function (event) {
          console.log(event.data);
          console.log("ON MESSAGE");
        }


      ws.onopen = () => {
         console.log("WebSocket now open...");
         console.log(ws.readyState);

         let i = 0;
         while (i<60){
            setInterval(gonder(i), 20000);
            i++;
         }

      };

      ws.onclose = () => {
            console.log("WebSocket now closed...");
            console.log(ws.readyState);
      };



    return (

            <Router history={hist}>
                <Switch>
                    <Route path="/rtl" component={RtlLayout} />
                    <Route path="/auth" component={AuthLayout} />
                    <Route path="/admin" component={AdminLayout} />
                    <Redirect from="/" to="/admin/dashboard" />
                </Switch>
            </Router>

    )
}
