
import { Page } from "./IAbcLicCheckState";

export const MenuOptions: Array<Page> = [
    {
      key: 1,
      text: "Manage Territories",
      name: "manage territories",
      type: "option",
      data: []
    },
    {
      key: 2,
      text: "Email Recipients",
      name: "email recipients",
      type: "option",
      data: []
    },
    {
      key: 3,
      text: "Download Logs",
      name: "download logs",
      type: "option",
      data: []
    },
  ];

// TODO Add headers to each report (columns)
export const Reports: Array<Page> = [
    {
      key: 1,
      text: "Dashboard",
      name: "dashboard",
      type: "dashboard",
      data: []
    },
    {
      key: 2,
      text: "Status Changes",
      name: "status changes",
      type: "report",
      data: []
    },
    {
      key: 3,
      text: "Issued Licenses",
      name: "issued licenses",
      type: "report",
      data: []
    },
    {
      key: 4,
      text: "New Applications",
      name: "new applications",
      type: "report",
      data: []
    },
  ];