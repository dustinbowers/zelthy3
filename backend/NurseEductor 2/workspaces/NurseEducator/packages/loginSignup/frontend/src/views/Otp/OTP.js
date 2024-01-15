import React, { useState, useEffect, useContext } from "react";
import Button from "../../components/Button";
import { useNavigate } from "react-router-dom";
import useOTP from "../../hooks/useOTP";
import OTPField from "../../components/otpField";
import axios from "../../axiosConfig";
import GlobalContext from "../../context/GlobalContext";
import Card from "../../components/Card";
import { convertToHtml } from "../../utils/helper";

const otpFields = {
  otp1: "",
  otp2: "",
  otp3: "",
  otp4: "",
  otp5: "",
  otp6: "",
};

const OTP = () => {
  const [counter, setCounter] = useState(30);
  const { values, current, handleChange, handleKeyUp } = useOTP(otpFields);
  const {
    username,
    useExist,
    requestId,
    consentText,
    setOtp,
    alternateOTP,
    alternateUsername,
    logoUrl,
    headerText,
    paraText,
    setErrorMsg,
    setCanSkipAltUsrName,
    setAltUsrType,
    baseUrl,
    errorMsg,
    altUsrType,
    countryCode,
    usrNameTypes,
    mobileLogo
  } = useContext(GlobalContext);

  const navigate = useNavigate();

  const redirectToLogin = () => {
    if (alternateOTP) {
      setAltUsrType((!isNaN(alternateUsername) ? "mobile" : "email"))
      navigate("/verify-username");
    } else {
      navigate("/");
    } 
  };

  const verifyOTP = () => {

    let usr 
    if (usrNameTypes.includes("email") && usrNameTypes.includes("mobile")) {
      usr = username
    } else if(usrNameTypes.includes("email")){
      usr = username
    } else if(usrNameTypes.includes("mobile")){
      usr = countryCode + username
    }

    if (
      (
        values.otp1 +
        values.otp2 +
        values.otp3 +
        values.otp4 +
        values.otp5 +
        values.otp6
      )?.length !== 6
    ) {
      setErrorMsg("Please Enter Valid OTP");
      return;
    }
    setOtp(
      Number(
        values.otp1 +
          values.otp2 +
          values.otp3 +
          values.otp4 +
          values.otp5 +
          values.otp6
      )
    );
    let postData = {
      step: useExist
        ? "verify_login_otp"
        : alternateOTP
        ? "verify_alternate_username_otp"
        : "verify_signup_otp",
      request_id: requestId,
      // "username": "rajat1234@zelthy.com",
      otp: Number(
        values.otp1 +
          values.otp2 +
          values.otp3 +
          values.otp4 +
          values.otp5 +
          values.otp6
      ),
      username: usr,
    };
    if (!useExist) {
      postData.consent_text = consentText;
    }
    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("response data", response);
        if (response.data.next === "done") {
          window.location.href = "/app/home/";
        } else if (response.data.next === "verify_alternate_username") {
          setCanSkipAltUsrName(response.data.can_skip_alternate_username);
          setAltUsrType(response.data.to_get_alternate_username_type);
          navigate("/verify-username");
        }
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
    console.log("otp values", values);
  };

  const resendOTP = () => {
    let usr 
    if (usrNameTypes.includes("email") && usrNameTypes.includes("mobile")) {
      usr = username
    } else if(usrNameTypes.includes("email")){
      usr = username
    } else if(usrNameTypes.includes("mobile")){
      usr = countryCode + username
    }

    let postData = {
      step: useExist
        ? "resend_login_otp"
        : alternateOTP
        ? "resend_alternate_username_otp"
        : "resend_signup_otp",
      request_id: requestId,
      // "username": "rajat1234@zelthy.com",

      username: usr,
    };
    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("response data", response);
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
  };

  const usernameType = () => {

    if (!usrNameTypes.includes("email")){
      return "email"
    } else if (!usrNameTypes.includes("mobile")){
      return "mobile number"
    } else {
      return "username"
    }
  }

  const usernameType2 = () => {

    if (usrNameTypes.includes("email")){
      return "email"
    } else if (usrNameTypes.includes("mobile")){
      return "mobile number"
    } else {
      return "username"
    }

  }

  const usernameVal = () => {

    if (!usrNameTypes.includes("email")){
      return username
    } else if (!usrNameTypes.includes("mobile")){
      return countryCode + ' ' + username
    } else {
      return ""
    }


  }

  useEffect(() => {
    if (counter !== 0) {
      const timer =
        counter > 0 && setInterval(() => setCounter(counter - 1), 1000);
      return () => clearInterval(timer);
    }
  }, [counter]);

  useEffect(() => {
    setErrorMsg("");
    console.log("alt is sign up", alternateOTP, alternateUsername);
  }, []);

  return (
    <>
      <section className="h-full">
        <div className="md:container xl:px-16 md:mx-auto flex flex-wrap justify-between w-screen items-center md:h-full flex-col sm:flex-row">
          <div className="w-full hidden md:block lg:w-5/12 md:w-1/2 pr-0 text-center md:text-left text-white">
            <h1 class="title-font text-4xl">{convertToHtml(headerText)}</h1>
            <p class="leading-relaxed mt-4 text-lg">{convertToHtml(paraText)}</p>
          </div>
          {/* <div className="md:w-1/2 w-screen text-center pl-0 lg:pl-36 xl:pl-56"> */}
            <Card logoUrl={logoUrl} mobileLogo={mobileLogo} title="OTP">
              <div className="text-xl font-bold mt-2 lg:mt-10">Verify your {alternateOTP ? usernameType() : usernameType2()} </div>
              <div className="flex flex-row text-sm text-GrayText pb-4">
                <p>
                  Enter the OTP sent to{" "}
                  <span className="font-bold">
                 {alternateOTP ? (!isNaN(alternateUsername) ? countryCode + " " + alternateUsername : alternateUsername)  : usrNameTypes.includes("mobile") && altUsrType === "phone" ? countryCode + " " + username : username}
                  </span>{" "}
                  <span
                    className="text-primary cursor-pointer font-bold"
                    onClick={redirectToLogin}
                  >
                    Edit
                  </span>{" "}
                </p>
              </div>
              {/* </div> */}

              {/* <div> */}
              <div className="flex flex-col w-full">
                <div className="grid gap-4 grid-cols-6 items-center w-full justify-items-center text-center">
                  {Array.from(Object.keys(otpFields)).map((otp, index) => (
                    <OTPField
                      key={otp}
                      name={otp}
                      value={values[otp]}
                      isFocus={current === index}
                      onChange={(e) => handleChange(e, index)}
                      onKeyUp={(e) => handleKeyUp(e, index)}
                    />
                  ))}
                </div>
                {errorMsg?.length > 2 && (
                  <div className="text-errorText text-sm md:bg-white opacity-70">
                    {errorMsg}
                  </div>
                )}

                <div className="text-sm mt-4 mb-10 text-GrayText">
                  {counter === 0 ? (
                    <span
                      onClick={resendOTP}
                      className="text-primary cursor-pointer font-bold"
                    >
                      Resend OTP
                    </span>
                  ) : (
                    <span> Resend OTP in {counter} secs</span>
                  )}{" "}
                </div>

                <div className="absolute w-full bottom-0 mx-auto">
                  <Button
                    label={`Verify and ${useExist ? "Login" : "Signup"}`}
                    onClick={verifyOTP}
                    disabled={ (values.otp1 +
                      values.otp2 +
                      values.otp3 +
                      values.otp4 +
                      values.otp5 +
                      values.otp6
                    )?.length !== 6 }
                  />
                </div>

                {/* <div className="mt-2 text-sm">
                  Already a user?
                  <span
                    className="text-primary ml-1 font-bold cursor-pointer"
                    onClick={() => navigate("/")}
                  >
                    Login
                  </span>
                </div> */}
              </div>
            </Card>
          {/* </div> */}
        </div>
      </section>
    </>
  );
};

export default OTP;
