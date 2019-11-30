import React, {useState} from "react";
import axios from 'axios';
import {API_BASE_URL} from "assets/jss/material-dashboard-pro-react";

// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import InputAdornment from "@material-ui/core/InputAdornment";
import Icon from "@material-ui/core/Icon";

// @material-ui/icons
//import Face from "@material-ui/icons/Face";
import Email from "@material-ui/icons/Email";
// import LockOutline from "@material-ui/icons/LockOutline";

// core components
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import CardHeader from "components/Card/CardHeader.js";
import CardFooter from "components/Card/CardFooter.js";
import { withRouter } from 'react-router-dom';
import styles from "assets/jss/material-dashboard-pro-react/views/loginPageStyle.js";

const useStyles = makeStyles(styles);

function LoginPage(props) {
  const [cardAnimaton, setCardAnimation] = React.useState("cardHidden");
  setTimeout(function() {
    setCardAnimation("");
  }, 700);
  const classes = useStyles();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const [errorType, setErrorType] = useState("");



  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(username);
    console.log(password);
    if (username === "") {
        setError(true);
        setErrorType("Kullanıcı adı boş");
        console.log("kullanıcı adı boş...");
    }
    else if (password === "") {
      setError(true);
      setErrorType("Parola boş");
      console.log("parola boş...");
    }
    else {

          try {
            const res = await axios.post(`${API_BASE_URL}auth/login/`, {
                username_or_email: username,
                password: password
            });
            console.log("try içinde");
            console.log(res);
            const token = res.data.token;
            const userName = res.data.username;
            const firstName = res.data.first_name;
            const lastName = res.data.last_name;
            const picProfile = res.data.pic_profile;
            const userId = res.data.user_id;
            const email = res.data.email;
            localStorage.setItem('token', token);
            localStorage.setItem('userName', userName);
            localStorage.setItem('firstName', firstName);
            localStorage.setItem('lastName', lastName);
            localStorage.setItem('pic_profile', picProfile);
            localStorage.setItem('user_id', userId);
            localStorage.setItem('email', email);

          }
           catch (err) {
            console.log("catch içinde");
            console.log(err.response);
            console.log(err.response.data);
            console.log(err.response.status);
            console.log(err.response.data.error);
            setError(true);
            setErrorType(err.response.data.error);
            //console.log("bağlantı hatası...");
          }

          if (localStorage.token){
            props.history.push('/dashboard');
          }

    }
  }

  return (
    <div className={classes.container}>
      <GridContainer justify="center">
        <GridItem xs={12} sm={6} md={4}>
          <form>
            <Card login className={classes[cardAnimaton]}>
              <CardHeader
                className={`${classes.cardHeader} ${classes.textCenter}`}
                color="rose"
              >
                <h4 className={classes.cardTitle}>Log in</h4>
                <div className={classes.socialLine}>
                  {[
                    "fab fa-facebook-square",
                    "fab fa-twitter",
                    "fab fa-google-plus"
                  ].map((prop, key) => {
                    return (
                      <Button
                        color="transparent"
                        justIcon
                        key={key}
                        className={classes.customButtonClass}
                      >
                        <i className={prop} />
                      </Button>
                    );
                  })}
                </div>
              </CardHeader>
              <CardBody>

                <CustomInput
                  labelText="Eposta"
                  id="email"
                  value={username}
                  formControlProps={{
                    fullWidth: true
                  }}
                  inputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <Email className={classes.inputAdornmentIcon} />
                      </InputAdornment>
                    ),
                  onChange: (e) => setUsername(e.target.value)
                  }}
                  //onChange = { (e) => setUsername(e.target.value)}
                />
                <CustomInput
                  labelText="Parola"
                  id="password"
                  formControlProps={{
                    fullWidth: true
                  }}
                  inputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <Icon className={classes.inputAdornmentIcon}>
                          lock_outline
                        </Icon>
                      </InputAdornment>
                    ),
                    type: "password",
                    autoComplete: "off",
                    onChange: (e) => setPassword(e.target.value)
                  }}
                />
              </CardBody>
              <CardFooter className={classes.justifyContentCenter}>
                <Button color="rose" simple size="lg" block  onClick={(e)=> handleSubmit(e)}>
                  GİRİŞ
                </Button>
              </CardFooter>
              { error && <div style={{color:`red`}}>{errorType}</div>      }
            </Card>
          </form>
        </GridItem>
      </GridContainer>
    </div>
  );
}


export default withRouter(LoginPage);
