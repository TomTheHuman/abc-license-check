import * as React from "react";
import styles from "./styles/AbcLicCheck.module.scss";
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
        return <Dashboard data={testData} state={this.state} />;
      default:
        let page = "";
        for (var i = 0; i < this.state.pages.length; i++) {
          if (this.state.pages[i].name == this.state.currentPage.name) {
            page = this.state.pages[i];
          }
        }
        return <Report report={page} />;
    }
  }

  private handlePageOption(page: Page) {
    this.setState({
      currentPage: page,
    });
  }

  private handlePageButton() {
    this.setState({
      repMenuOpen: !this.state.repMenuOpen,
      optMenuOpen: false,
    });
  }

  private handleOptionsButton() {
    this.setState({
      repMenuOpen: false,
      optMenuOpen: !this.state.optMenuOpen,
    });
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

const NavOptions: any = {
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
      columns: {
        title: "Dashboard",
        width: "",
        data: "",
      },
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
  ],
};

const testData = {
  headers: {
    lic_num: "Lic. Num",
    status_from: "Status From",
    status_to: "Status To",
    lic_type: "Lic. Type",
    lic_dup: "Lic. Dup",
    issue_date: "Iss. Date",
    exp_date: "Exp. Date",
    acct_name: "Account Name",
    acct_own: "Account Owner",
    acct_street: "Account Street",
    acct_city: "Account City",
    acct_state: "Account State",
    acct_zip: "Account Zip",
    mail_street: "Mail Street",
    mail_city: "Mail City",
    mail_state: "Mail State",
    mail_zip: "Mail Zip",
    trans_from: "Trans From",
    trans_to: "Trans To",
    geocode: "Geocode",
  },
  data: [
    {
      acct_city: "Grundy",
      acct_name: "And at first, this sort ofthing is unpleasant enough.",
      acct_own: "Antwon Abshire",
      acct_state: "New Jersey",
      acct_street: "Broad Street",
      acct_zip: "77549",
      exp_date: "2075-02-21",
      geocode: 555,
      issue_date: "2076-08-03",
      lic_dup: "tzwmn",
      lic_num: 242,
      lic_type: "lcjfq",
      mail_city: "Beasley",
      mail_state: "Maine",
      mail_street: "5th Street South",
      mail_zip: "97567",
      status_from: "2032-05-12",
      status_to: "2074-10-16",
      trans_from: "iwwwm",
      trans_to: "oznem",
    },
  ],
};
