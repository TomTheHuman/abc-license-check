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

  public componentDidMount() {}

  private _handlePage() {
    switch (this.state.currentPage.type) {
      case "dashboard":
        return <Dashboard state={this.state} />;
      case "report":
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
