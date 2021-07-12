import * as React from "react";
import styles from "./styles/AbcLicCheck.module.scss";
import { IAbcLicCheckProps } from "./IAbcLicCheckProps";
import { IAbcLicCheckState, Page } from "./IAbcLicCheckState";
import Navigation from "./Navigation";
import Dashboard from "./Dashboard";
import Report from "./Report";
import axios from "axios";
import { escape } from "@microsoft/sp-lodash-subset";
import { ISPHttpClientOptions, SPHttpClient, HttpClient, SPHttpClientResponse } from "@microsoft/sp-http";

export default class AbcLicCheck extends React.Component<
  IAbcLicCheckProps,
  IAbcLicCheckState
> {
  public constructor(props: IAbcLicCheckProps) {
    super(props);

    this.state = {
      currentPage: Reports[0],
      menuOptions: MenuOptions,
      reports: Reports,
    };

    this.handlePage = this.handlePage.bind(this);
    this.setPage = this.setPage.bind(this);
  }

  public componentDidMount() {
    const urlStatusChange = "http://localhost:8000/api/v1/reports/status_change/"
    const urlNewApplication = "http://localhost:8000/api/v1/reports/new_application/"
    const urlIssuedLicense = "http://localhost:8000/api/v1/reports/issued_license/"

    const reqStatusChange = axios.get(urlStatusChange);
    const reqNewApplication = axios.get(urlNewApplication);
    const reqIssuedLicense = axios.get(urlIssuedLicense);

    axios.all([reqStatusChange, reqNewApplication, reqIssuedLicense])
    .then((res) => {
      const resStatusChange = res[0].data;
      const resNewApplication = res[1].data;
      const resIssuedLicense = res[2].data;

      const reports = this.state.reports;
      const reportsData = reports.map((report) => {
        console.log(report)
        switch (report.name) {
          case "status changes":
            report.data = resStatusChange;
            return report;
          case "new applicatons":
            report.data = resNewApplication;
            return report;
          case "issued licenses":
            report.data = resIssuedLicense;
            return report;
          default:
            break;
        }
      });
      console.log(reportsData)
      this.setState(() => {
        reports: reportsData
      }, () => console.log(this.state.reports))
    })

  }

  private handlePage() {
    switch (this.state.currentPage.type) {
      case "dashboard":
        return <Dashboard state={this.state} />;
      case "report":
        return <Report state={this.state} />;
      default:
        // Return specific pages
    }
  }

  private setPage(page: Page) {
    this.setState({
      currentPage: page,
    });
  }

  public render(): React.ReactElement<IAbcLicCheckProps> {
    return (
      <div className={`${""} ms-Grid`}>
          <Navigation
            state={this.state}
            setPage={this.setPage}
          />
        <div className="ms-Grid-row">
          <div className={""}>{this.handlePage()}</div>
        </div>
      </div>
    );
  }
}

const MenuOptions: Array<Page> = [
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
]

const Reports: Array<Page> = [
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
]
