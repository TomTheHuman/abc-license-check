import * as React from "react";
import styles from "./styles/Dashboard.module.scss";
import Table from "./Table";

// BIG BRAIN DEV UPDATE

const Dashboard = ({ data, state }) => {
  return (
    <div className={styles.dashboard}>
      <Table data={data} />
    </div>
  );
};

export default Dashboard;
