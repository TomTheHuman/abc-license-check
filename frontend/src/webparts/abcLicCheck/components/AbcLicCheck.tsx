import * as React from "react";
import styles from "./AbcLicCheck.module.scss";
import { IAbcLicCheckProps } from "./IAbcLicCheckProps";
import { IAbcLicCheckState, Page } from "./IAbcLicCheckState";
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
      currentPage: NavOptions.reports[0],
      repMenuOpen: false,
      optMenuOpen: false,
      options: NavOptions.options,
      pages: NavOptions.reports,
    };

    this.handlePage = this.handlePage.bind(this);
    this.handlePageOption = this.handlePageOption.bind(this);
    this.handlePageButton = this.handlePageButton.bind(this);
    this.handleOptionsButton = this.handleOptionsButton.bind(this);
  }

  private handlePage() {

    switch (this.state.currentPage.name) {
      case "dashboard":
        return <Dashboard state={this.state} />;
      default:
        let report = "";
        for (var i = 0; i < this.state.pages.length; i++) {
          if (this.state.pages[i].name == this.state.currentPage.name) {
            report = this.state.pages[i];
          }
        }
        return <Report report={report} />;
    }
  }

  private handlePageOption(page: Page) {
    this.setState({
      currentPage: page,
    });
  }

  private handlePageButton() {
    this.setState(
      {
        repMenuOpen: !this.state.repMenuOpen,
        optMenuOpen: false,
      });
  }

  private handleOptionsButton() {
    this.setState(
      {
        repMenuOpen: false,
        optMenuOpen: !this.state.optMenuOpen,
      }
    );
  }

  public render(): React.ReactElement<IAbcLicCheckProps> {
    return (
      <div className={styles.abcLicCheck}>
        <Navigation
          state={this.state}
          handlePageOption={this.handlePageOption}
          handlePageButton={this.handlePageButton}
          handleOptionsButton={this.handleOptionsButton}
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
        name: "dashboard",
        formalName: "Dashboard",
      },
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