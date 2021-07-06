import * as React from "react";
import styles from "./styles/Report.module.scss";

const Report = ({ report }) => {
  return (
    <div className={styles.report}>
      <h1>{report.formalName} data...</h1>
    </div>
  );
};

export default Report;
