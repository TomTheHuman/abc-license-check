export interface Page {
  key: number;
  text: string;
  name: string;
  type: string;
}

export interface Report {
  key: number;
  text: string;
  name: string;
  type: string;
  headers: Array<Header>;
}

export interface Header {
  key: string;
  text: string;
  filter: boolean;
}

export interface IItem {
  id: number;
  report_date: Date;
  report_type: string;
  lic_num: number;
  status_from: string;
  status_to: string;
  status: string;
  lic_type: string;
  lic_dup: string;
  issue_date: Date;
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
  conditions: string;
  escrow_addr: string;
  district: string;
  trans_from: string;
  trans_to: string;
  geocode: number;
}

export interface IAbcLicCheckState {
  currentPage: Page;
  menuOptions: Array<Page>;
  reports: Array<Report>;
}
