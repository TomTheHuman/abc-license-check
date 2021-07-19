import * as React from "react";
import { DataList } from "./DataList";
import styles from "./styles/Report.module.scss";

const Report = ({ report }) => {
  return (
    <div className={styles.report}>
      <DataList report={report} />
    </div>
  );
};

export default Report;