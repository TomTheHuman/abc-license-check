import * as React from "react";
import styles from "./styles/AbcLicCheck.module.scss";
import { IAbcLicCheckProps } from "./IAbcLicCheckProps";
import { IAbcLicCheckState, Page } from "./IAbcLicCheckState";
import { Reports, MenuOptions } from "./Options";
import Navigation from "./Navigation";
import Dashboard from "./Dashboard";
import Report from "./Report";
import axios from "axios";

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

    this._handlePage = this._handlePage.bind(this);
    this._setPage = this._setPage.bind(this);
  }

  // TODO Get API to serve data sorted by created date
  public componentDidMount() {
    const urlStatusChange =
      "http://localhost:8000/api/v1/reports/status_change/";
    const urlNewApplication =
      "http://localhost:8000/api/v1/reports/new_application/";
    const urlIssuedLicense =
      "http://localhost:8000/api/v1/reports/issued_license/";

    const reqStatusChange = axios.get(urlStatusChange);
    const reqNewApplication = axios.get(urlNewApplication);
    const reqIssuedLicense = axios.get(urlIssuedLicense);

    axios
      .all([reqStatusChange, reqNewApplication, reqIssuedLicense])
      .then((res) => {
        const resStatusChange = res[0].data;
        const resNewApplication = res[1].data;
        const resIssuedLicense = res[2].data;

        const reports = this.state.reports;
        const reportsData = reports.map((report) => {
          switch (report.name) {
            case "status changes":
              report.data = resStatusChange;
              return report;
            case "new applications":
              report.data = resNewApplication;
              return report;
            case "issued licenses":
              report.data = resIssuedLicense;
              return report;
            default:
              break;
          }
        });
        this.setState(() => {
          reports: reportsData;
        });
      });
  }

  private _handlePage() {
    switch (this.state.currentPage.type) {
      case "dashboard":
        return <Dashboard state={this.state} />;
      case "report":
        // console.log("Running!");
        return <Report report={this.state.currentPage} />;
      default:
      // Return specific pages
    }
  }

  private _setPage(page: Page) {
    this.setState({
      currentPage: page,
    });
  }

  public render(): React.ReactElement<IAbcLicCheckProps> {
    console.log(this.state.currentPage);
    return (
      // TODO Make this div resize based on height of window
      <div className={`${styles.abcLicCheck} ms-Grid`}>
        <Navigation state={this.state} setPage={this._setPage} />
        <div className="ms-Grid-row">
          <div
            id={`report-${this.state.currentPage.name}`}
            className={"ms-Grid-col ms-sm12"}
          >
            {this._handlePage()}
          </div>
        </div>
      </div>
    );
  }
}
