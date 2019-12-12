import React, { useState } from 'react';
import MainContext from './MainContext';

export default function MainProvider(props) {
  const [kuryeler, setKuryeler]  = useState([]);


  return (
      <MainContext.Provider
          value={{
              kuryeler: kuryeler,
              updateKuryeler: [...kuryeler]
          }}
      >
          {props.children}
      </MainContext.Provider>
  );

}
