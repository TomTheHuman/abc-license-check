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
    const urlStatusChange_All =
      "http://localhost:8000/api/v1/reports/status_change/";
    const urlStatusChange_Today =
      "http://localhost:8000/api/v1/reports/status_change/today";
    const urlNewApplication_All =
      "http://localhost:8000/api/v1/reports/new_application/";
    const urlNewApplication_Today =
      "http://localhost:8000/api/v1/reports/new_application/today";
    const urlIssuedLicense_All =
      "http://localhost:8000/api/v1/reports/issued_license/";
    const urlIssuedLicense_Today =
      "http://localhost:8000/api/v1/reports/issued_license/today";

    // const reqStatusChange_Today = axios.get(urlStatusChange_Today);
    const reqStatusChange_All = axios.get(urlStatusChange_All);
    // const reqNewApplication_Today = axios.get(urlNewApplication_Today);
    const reqNewApplication_All = axios.get(urlNewApplication_All);
    // const reqIssuedLicense_Today = axios.get(urlIssuedLicense_Today);
    const reqIssuedLicense_All = axios.get(urlIssuedLicense_All);

    axios
      .all([
        reqStatusChange_All,
        // reqStatusChange_Today,
        reqNewApplication_All,
        // reqNewApplication_Today,
        reqIssuedLicense_All,
        // reqIssuedLicense_Today,
      ])
      .then((res) => {
        const resStatusChange_All = res[0].data;
        const resStatusChange_Today = res[1].data;
        const resNewApplication_All = res[2].data;
        // const resNewApplication_Today = res[3].data;
        // const resIssuedLicense_All = res[4].data;
        // const resIssuedLicense_Today = res[5].data;

        const reports = this.state.reports;
        const reportsData = reports.map((report) => {
          switch (report.name) {
            case "status changes":
              report.data.all = resStatusChange_All;
              report.data.today = resStatusChange_Today;
              return report;
            case "new applications":
              report.data.all = resNewApplication_All;
              // report.data.today = resNewApplication_Today;
              return report;
            case "issued licenses":
              // report.data.all = resIssuedLicense_All;
              // report.data.today = resIssuedLicense_Today;
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
