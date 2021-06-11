import * as React from "react";
import styles from "./AbcLicCheck.module.scss";
import { IAbcLicCheckProps } from "./IAbcLicCheckProps";
import { IAbcLicCheckState } from "./IAbcLicCheckState";
import Navigation from "./Navigation";
import Dashboard from "./Dashboard";
import Report from "./Report";
import { escape } from "@microsoft/sp-lodash-subset";

export default class AbcLicCheck extends React.Component<
  IAbcLicCheckProps,
  IAbcLicCheckState
> {
  public constructor(props: IAbcLicCheckProps) {
    super(props);

    this.state = {
      currentPage: "dashboard",
      menuOpen: false,
      options: NavOptions.options,
      pages: NavOptions.reports,
    };

    this.handlePage = this.handlePage.bind(this);
    this.handlePageButton = this.handlePageButton.bind(this);
    this.handleOptionButton = this.handleOptionButton.bind(this);
  }

  private handlePage() {

    switch (this.state.currentPage) {
      case "dashboard":
        return <Dashboard state={this.state} />;
      default:
        let report = "";
        for (var i = 0; i < this.state.pages.length; i++) {
          if (this.state.pages[i].name == this.state.currentPage) {
            report = this.state.pages[i];
          }
        }
        return <Report report={report} />;
    }
  }

  private handlePageButton(pageName: string) {
    this.setState({
      currentPage: pageName,
    });
  }

  private handleOptionButton() {
    this.setState(
      {
        menuOpen: !this.state.menuOpen,
      }
    );
  }

  public render(): React.ReactElement<IAbcLicCheckProps> {
    return (
      <div className={styles.abcLicCheck}>
        <Navigation
          handlePageButton={this.handlePageButton}
          handleOptionButton={this.handleOptionButton}
          state={this.state}
        />
        <div className={styles.contentContainer}>{this.handlePage()}</div>
      </div>
    );
  }
}

const NavOptions:any = {
    options: [
      {
        name: "manage territories",
        formalName: "Manage Territories",
      },
      {
        name: "email recipients",
        formalName: "Email Recipients",
      },
      {
        name: "download logs",
        formalName: "Download Logs",
      },
    ],
    reports: [
      {
        name: "status changes",
        formalName: "Status Changes",
      },
      {
        name: "issued licenses",
        formalName: "Issued Licenses",
      },
      {
        name: "new applications",
        formalName: "New Applications",
      },
    ]
  }