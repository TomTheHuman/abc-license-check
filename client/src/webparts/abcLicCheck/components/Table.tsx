import * as React from "react";
import styles from "./styles/Table.module.scss";

import {
  AddBox,
  ArrowDownward,
  DeleteForeverRounded,
  FilterListRounded,
} from "@material-ui/icons";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  Toolbar,
  Typography,
  Paper,
  IconButton,
  Tooltip,
  FormControlLabel,
  Switch,
} from "@material-ui/core";

interface Data {
  lic_num: number;
  status_from: Date;
  status_to: Date;
  lic_type: string;
  lic_dup: string;
  issue_date: string;
  exp_date: Date;
  acct_name: string;
  acct_own: string;
  acct_street: string;
  acct_city: string;
  acct_state: string;
  acct_zip: string;
  mail_street: string;
  mail_city: string;
  mail_state: string;
  mail_zip: string;
  trans_from: string;
  trans_to: string;
  geocode: string;
}

const DataTable = ({ data }) => {
  return <div className={styles.tableContainer}></div>;
};

export default DataTable;
