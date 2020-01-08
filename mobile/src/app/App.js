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

      function gonder1(i){
          let y = i*0.001;
          // Göztepe parkı
          //var lat = 40.970894;
          //var lon = 29.056185;
          // Archerson
          //var lat = 40.998820;
          //var lon = 29.087562;

          var lat = 40.908820;
          var lon = 29.007562;
          var lat_new = lat + y;
          var lon_new = lon + y;
          var msg = {
              type: "send_location",
              latitude: lat_new,
              longitude:lon_new,
            };
            console.log(i)
           if (ws1.readyState === WebSocket.OPEN) {
               ws1.send(JSON.stringify(msg));
           }
        }

        function gonder2(i){
            let y = i*0.001;
            // Göztepe parkı
            //var lat = 40.970894;
            //var lon = 29.056185;
            // Archerson
            //var lat = 40.998820;
            //var lon = 29.087562;

            var lat1 = 40.906820;
            var lon1 = 29.005562;
            var lat2 = 40.908820;
            var lon2 = 29.007562;

            var lat_new1 = lat1 + y;
            var lon_new1 = lon1 + y;
            var lat_new2 = lat2 + y;
            var lon_new2 = lon2 + y;
            var msg1 = {
                type: "send_location",
                latitude: lat_new1,
                longitude:lon_new1,
              };
              var msg2 = {
                  type: "send_location",
                  latitude: lat_new2,
                  longitude:lon_new2,
                };
              console.log(i)
            if (ws1.readyState === WebSocket.OPEN) {
                  ws1.send(JSON.stringify(msg1));
              }
             if (ws2.readyState === WebSocket.OPEN) {
                 ws2.send(JSON.stringify(msg2));
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
      const newToken1 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwOTk0Mzg1OCwianRpIjoiYzRkZTViYWE4ZDEzNDBlODhiZjAyMTIxNDJjOGYzMjkiLCJ1c2VyX2lkIjoyfQ.4DHSel-3y1drbMvgmydOtaLfRQ9xVYNAqhSIK6ZZJN0";
      //let newToken = retrieveToken(token)
      //const newToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc0OTQ3NzkxLCJqdGkiOiIwNWM4MjhjZTUzMjY0YmRhYjY5YWIxYjJmNmNmZDMxMiIsInVzZXJfaWQiOjJ9.dtFi9MB71ug3OvUb04NTA6GFQPnjVuRSkSFovsqNLSU";
      console.log(newToken1);
      const newToken2 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwOTk0Mzk0MiwianRpIjoiNTQwZjMwZTUzZDBlNDgwN2JhYjMzYjFlY2JlNTUyMDgiLCJ1c2VyX2lkIjozfQ.tS2gIJoYlZcDrRb_5w_JJTWAVRPZPtZesQvSdlp5ano";
      console.log(newToken2);

      let endpoint = `${WS_BASE_URL}kurye/`
      //let endpoint = "ws://127.0.0.1:8000/kurye/"
      // Create new WebSocket
      let ws1 = new WebSocket(endpoint + "?token=" + newToken1)
      let ws2 = new WebSocket(endpoint + "?token=" + newToken2)

      ws1.onmessage = function (event) {
          console.log(event.data);
          console.log("ON MESSAGE-1");
        }
      ws2.onmessage = function (event) {
          console.log(event.data);
          console.log("ON MESSAGE-2");
        }
      /*
      ws1.onopen = () => {
         console.log("WebSocket now open...");
         console.log(ws1.readyState);
         let i = 0;
         while (i<60){
            setInterval(gonder1(i), 20000);
            i++;
         }
      };
      */
      ws2.onopen = () => {
         console.log("WebSocket now open...");
         console.log(ws2.readyState);
         let i = 0;
         while (i<60){
            setInterval(gonder2(i), 20000);
            i++;
         }
      };
      ws1.onclose = () => {
            console.log("WebSocket now closed...");
            console.log(ws1.readyState);
      };
      ws2.onclose = () => {
            console.log("WebSocket now closed...");
            console.log(ws2.readyState);
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
