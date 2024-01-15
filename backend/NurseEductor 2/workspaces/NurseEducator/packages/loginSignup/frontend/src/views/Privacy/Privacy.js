import React, {useEffect} from 'react'
import axios from '../../axiosConfig'


const Privacy = () => {

    useEffect(() => {
        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());

        let queryParams = [];
    Object.keys(params).forEach((element) => {
      queryParams.push(element + "=" + params[element]);
    });

    let queryString = "";
    for (let i = 0; i < queryParams.length; i++) {
      const element = queryParams[i];
      queryString += element + "&";
    }

    queryString = queryString.substring(0, queryString.length - 1);
    console.log("query params", queryParams, queryString);

    console.log("addressbar path", window.location.pathname.split("/"));

    let pathName = window.location.pathname.split("/");
    console.log(
      "pathname",
      window.location.origin
    );

        axios
        .get(`/${pathName[3]}/${queryString.length > 0 ? '?' + queryString : ''}`)
        .then((response) => {
          
            document.getElementById("privacy-data").insertAdjacentHTML('beforeend', response.data.theme_config.privacy_policy);
        });
    }, [])
    
 
    
  return (
    <div className='w-screen h-screen bg-white relative z-40'>
        <div class="overflow-y-scroll p-4" id="privacy-data"></div>
    </div>
  )
}

export default Privacy