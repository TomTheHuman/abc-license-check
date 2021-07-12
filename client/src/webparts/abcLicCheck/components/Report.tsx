import * as React from "react";
import styles from "./styles/Report.module.scss";

const Report = ({ state }) => {
  return (
    <div className={""}>
      <h1>{state.currentPage.text} data...</h1>
    </div>
  );
};

export default Report;
