import { Page, Report, Header } from "./IAbcLicCheckState";

export const MenuOptions: Array<Page> = [
  {
    key: 1,
    text: "Manage Territories",
    name: "manage territories",
    type: "option",
  },
  {
    key: 2,
    text: "Email Recipients",
    name: "email recipients",
    type: "option",
  },
  {
    key: 3,
    text: "Download Logs",
    name: "download logs",
    type: "option",
  },
];

export const Reports: Array<Report> = [
  {
    key: 0,
    text: "Dashboard",
    name: "dashboard",
    type: "dashboard",
    headers: null,
  },
  {
    key: 1,
    text: "Status Changes",
    name: "status_change",
    type: "report",
    headers: [
      { key: "report_date", text: "Report Date", filter: false },
      { key: "report_type", text: "Report Type", filter: false },
      { key: "lic_num", text: "License Number", filter: true },
      { key: "status_from", text: "Status from", filter: true },
      { key: "status_to", text: "Status To", filter: true },
      { key: "lic_type", text: "License Type", filter: true },
      { key: "lic_dup", text: "License Dup.", filter: true },
      { key: "issue_date", text: "Issue Date", filter: false },
      { key: "exp_date", text: "Expiration Date", filter: false },
      { key: "acct_name", text: "Account Name", filter: true },
      { key: "acct_own", text: "Account Owner", filter: true },
      { key: "acct_street", text: "Account Street", filter: true },
      { key: "acct_city", text: "Account City", filter: true },
      { key: "acct_state", text: "Account State", filter: true },
      { key: "acct_zip", text: "Account Zip", filter: true },
      { key: "mail_street", text: "Mail Street", filter: true },
      { key: "mail_city", text: "Mailting City", filter: true },
      { key: "mail_state", text: "Mail State", filter: true },
      { key: "mail_zip", text: "Mail Zip", filter: true },
      { key: "trans_from", text: "Trans. From", filter: true },
      { key: "trans_to", text: "Trans. To", filter: true },
      { key: "district", text: "District", filter: true },
      { key: "geocode", text: "Geocode", filter: true },
    ],
  },
  {
    key: 2,
    text: "Issued Licenses",
    name: "issued_license",
    type: "report",
    headers: [
      { key: "report_date", text: "Report Date", filter: false },
      { key: "report_type", text: "Report Type", filter: false },
      { key: "lic_num", text: "License Number", filter: true },
      { key: "status", text: "Status", filter: true },
      { key: "lic_type", text: "License Type", filter: true },
      { key: "lic_dup", text: "License Dup.", filter: true },
      { key: "exp_date", text: "Expiration Date", filter: false },
      { key: "acct_name", text: "Account Name", filter: true },
      { key: "acct_own", text: "Account Owner", filter: true },
      { key: "acct_street", text: "Account Street", filter: true },
      { key: "acct_city", text: "Account City", filter: true },
      { key: "acct_state", text: "Account State", filter: true },
      { key: "acct_zip", text: "Account Zip", filter: true },
      { key: "mail_street", text: "Mail Street", filter: true },
      { key: "mail_city", text: "Mailting City", filter: true },
      { key: "mail_state", text: "Mail State", filter: true },
      { key: "mail_zip", text: "Mail Zip", filter: true },
      { key: "action", text: "Action", filter: true },
      { key: "conditions", text: "Conditions", filter: true },
      { key: "escrow", text: "Escrow", filter: true },
      { key: "district", text: "District", filter: true },
      { key: "geocode", text: "Geocode", filter: true },
    ],
  },
  {
    key: 3,
    text: "New Applications",
    name: "new_application",
    type: "report",
    headers: [
      { key: "report_date", text: "Report Date", filter: false },
      { key: "report_type", text: "Report Type", filter: false },
      { key: "lic_num", text: "License Number", filter: true },
      { key: "status", text: "Status", filter: true },
      { key: "lic_type", text: "License Type", filter: true },
      { key: "lic_dup", text: "License Dup.", filter: true },
      { key: "exp_date", text: "Expiration Date", filter: false },
      { key: "acct_name", text: "Account Name", filter: true },
      { key: "acct_own", text: "Account Owner", filter: true },
      { key: "acct_street", text: "Account Street", filter: true },
      { key: "acct_city", text: "Account City", filter: true },
      { key: "acct_state", text: "Account State", filter: true },
      { key: "acct_zip", text: "Account Zip", filter: true },
      { key: "mail_street", text: "Mail Street", filter: true },
      { key: "mail_city", text: "Mailting City", filter: true },
      { key: "mail_state", text: "Mail State", filter: true },
      { key: "mail_zip", text: "Mail Zip", filter: true },
      { key: "action", text: "Action", filter: true },
      { key: "conditions", text: "Conditions", filter: true },
      { key: "escrow", text: "Escrow", filter: true },
      { key: "district", text: "District", filter: true },
      { key: "geocode", text: "Geocode", filter: true },
    ],
  },
];
