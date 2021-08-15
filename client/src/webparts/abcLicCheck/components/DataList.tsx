import * as React from "react";
import axios from "axios";
import { Page, Report, Header, IItem } from "./IAbcLicCheckState";
import { TextField } from "@fluentui/react/lib/TextField";
import { Toggle } from "@fluentui/react/lib/Toggle";
import { Announced } from "@fluentui/react/lib/Announced";
import {
  DetailsList,
  DetailsListLayoutMode,
  Selection,
  SelectionMode,
  IColumn,
  IDetailsColumnRenderTooltipProps,
  IDetailsHeaderProps,
  IDetailsListStyles,
  IViewport,
} from "@fluentui/react/lib/DetailsList";
import { MarqueeSelection } from "@fluentui/react/lib/MarqueeSelection";
import {
  Dropdown,
  IDropdownOption,
  IIconProps,
  IconButton,
  ThemeProvider,
  ScrollablePane,
  PrimaryButton,
} from "office-ui-fabric-react";
import { TooltipHost } from "@fluentui/react/lib/Tooltip";
import { IRenderFunction } from "@fluentui/react/lib/Utilities";
import Pagination from "office-ui-fabric-react-pagination";
import styles from "./styles/DetailsList.module.scss";
import { StylesProvider } from "@material-ui/styles";
import { useState } from "react";

export interface DetailsListState {
  offset: number;
  limit: IDropdownOption;
  columns: Object;
  filteredColumns: IColumn[];
  items: IItem[];
  selectionDetails: string;
  isCompactMode: boolean;
  isToday: boolean;
  showControl: boolean;
  isFiltered: boolean;
  colFilters: Array<Header>;
  selectedFilters: Object;
  announcedMessage?: string;
  report: Report;
  height: number;
  currentPage: number;
  pageCount: number;
}

export class DataList extends React.Component<
  { report: Report },
  DetailsListState
> {
  private _selection: Selection;
  private _items: IItem[];
  private _itemsAll: IItem[];
  private _itemsToday: IItem[];
  private _headers: Array<Header>;
  private _apiURL: string;
  private _limitChoices: Array<IDropdownOption>;

  constructor(props: { report: Report }) {
    super(props);
    this._headers = this.props.report.headers;

    // API URL for current page of data
    this._apiURL = `http://localhost:8000/api/v1/reports/${this.props.report.name}/`;
    this._limitChoices = [
      { key: 10, text: "10" },
      { key: 25, text: "25" },
      { key: 50, text: "50" },
      { key: 75, text: "75" },
      { key: 100, text: "100" },
    ];

    this._updateWindowDimensions = this._updateWindowDimensions.bind(this);

    const columns: Object = {
      report_date: {
        key: "report_date",
        name: "Report Date",
        fieldName: "report_date",
        data: "date",
        ariaLabel:
          "Column operations for Report Date, Press to sort on Report Date",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: true,
        sortAscendingAriaLabel: "Sorted Older to Newer",
        sortDescendingLabel: "Sorted Newer to Older",
        onColumnClick: this._onColumnClick,
        isPadded: true,
        onRender: (item: IItem) => {
          let newDate = new Date(String(item.report_date));
          return (
            <span>{`${
              newDate.getMonth() + 1
            }/${newDate.getDate()}/${newDate.getFullYear()}`}</span>
          );
        },
      },
      report_type: {
        key: "report_type",
        name: "Report Type",
        fieldName: "report_type",
        data: "string",
        ariaLabel:
          "Column operations for Report Type, Press to sort on Report Type",
        isResizable: true,
        isRowHeader: true,
        minWidth: 120,
        maxWidth: 260,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      lic_num: {
        key: "lic_num",
        name: "License Number",
        fieldName: "lic_num",
        data: "number",
        ariaLabel:
          "Column operations for License Number, Press to sort on License Number",
        isResizable: true,
        isRowHeader: true,
        minWidth: 100,
        maxWidth: 260,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted Lowest to Highest",
        sortDescendingLabel: "Sorted Highest to Lowest",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      status_from: {
        key: "status_from",
        name: "Status From",
        fieldName: "status_from",
        data: "string",
        ariaLabel:
          "Column operations for Status From, Press to sort on Status From",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      status_to: {
        key: "status_to",
        name: "Status To",
        fieldName: "status_to",
        data: "string",
        ariaLabel:
          "Column operations for Status To, Press to sort on Status To",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      status: {
        key: "status",
        name: "Status",
        fieldName: "status",
        data: "string",
        ariaLabel: "Column operations for Status, Press to sort on Status",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      lic_type: {
        key: "lic_type",
        name: "License Type",
        fieldName: "lic_type",
        data: "string",
        ariaLabel:
          "Column operations for License Type, Press to sort on License Type",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      lic_dup: {
        key: "lic_dup",
        name: "License Dup.",
        fieldName: "lic_dup",
        data: "string",
        ariaLabel:
          "Column operations for License Dup., Press to sort on License Dup.",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      issue_date: {
        key: "issue_date",
        name: "Issue Date",
        fieldName: "issue_date",
        data: "date",
        ariaLabel:
          "Column operations for Issue Date, Press to sort on Issue Date",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted Older to Newer",
        sortDescendingLabel: "Sorted Newer to Older",
        onColumnClick: this._onColumnClick,
        isPadded: true,
        onRender: (item: IItem) => {
          if (item.issue_date) {
            let newDate = new Date(String(item.issue_date));
            return (
              <span>{`${
                newDate.getMonth() + 1
              }/${newDate.getDate()}/${newDate.getFullYear()}`}</span>
            );
          }
        },
      },
      exp_date: {
        key: "exp_date",
        name: "Expiration Date",
        fieldName: "exp_date",
        data: "date",
        ariaLabel:
          "Column operations for Expiration Date, Press to sort on Expiration Date",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted Older to Newer",
        sortDescendingLabel: "Sorted Newer to Older",
        onColumnClick: this._onColumnClick,
        isPadded: true,
        onRender: (item: IItem) => {
          if (item.exp_date) {
            let newDate = new Date(String(item.exp_date));
            return (
              <span>{`${
                newDate.getMonth() + 1
              }/${newDate.getDate()}/${newDate.getFullYear()}`}</span>
            );
          }
        },
      },
      acct_name: {
        key: "acct_name",
        name: "Account Name",
        fieldName: "acct_name",
        data: "string",
        ariaLabel:
          "Column operations for Account Name, Press to sort on Account Name",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_own: {
        key: "acct_own",
        name: "Account Owner",
        fieldName: "acct_own",
        data: "string",
        ariaLabel:
          "Column operations for Account Owner, Press to sort on Account Owner",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_street: {
        key: "acct_street",
        name: "Account Street",
        fieldName: "acct_street",
        data: "string",
        ariaLabel:
          "Column operations for Account Street, Press to sort on Account Street",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_city: {
        key: "acct_city",
        name: "Account City",
        fieldName: "acct_city",
        data: "string",
        ariaLabel:
          "Column operations for Account City, Press to sort on Account City",
        isResizable: true,
        isRowHeader: true,
        minWidth: 160,
        maxWidth: 320,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_state: {
        key: "acct_state",
        name: "Account State",
        fieldName: "acct_state",
        data: "string",
        ariaLabel:
          "Column operations for Account State, Press to sort on Account State",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_zip: {
        key: "acct_zip",
        name: "Account Zip",
        fieldName: "acct_zip",
        data: "string",
        ariaLabel:
          "Column operations for Account Zip, Press to sort on Account Zip",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      mail_street: {
        key: "mail_street",
        name: "Mail Street",
        fieldName: "mail_street",
        data: "string",
        ariaLabel:
          "Column operations for Mail Street, Press to sort on Mail Street",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      mail_city: {
        key: "mail_city",
        name: "Mail City",
        fieldName: "mail_city",
        data: "string",
        ariaLabel:
          "Column operations for Mail City, Press to sort on Mail City",
        isResizable: true,
        isRowHeader: true,
        minWidth: 160,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      mail_state: {
        key: "mail_state",
        name: "Mail State",
        fieldName: "mail_state",
        data: "string",
        ariaLabel:
          "Column operations for Mail State, Press to sort on Mail State",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      mail_zip: {
        key: "mail_zip",
        name: "Mail Zip",
        fieldName: "mail_zip",
        data: "string",
        ariaLabel: "Column operations for Mail Zip, Press to sort on Mail Zip",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      action: {
        key: "action",
        name: "Action",
        fieldName: "action",
        data: "string",
        ariaLabel: "Column operations for Action, Press to sort on Action",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      conditions: {
        key: "conditions",
        name: "Conditions",
        fieldName: "conditions",
        data: "string",
        ariaLabel:
          "Column operations for Conditions, Press to sort on Conditions",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      escrow: {
        key: "escrow",
        name: "Escrow",
        fieldName: "escrow",
        data: "string",
        ariaLabel: "Column operations for Escrow, Press to sort on Escrow",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      district: {
        key: "district",
        name: "District",
        fieldName: "district",
        data: "string",
        ariaLabel: "Column operations for District, Press to sort on District",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      trans_from: {
        key: "trans_from",
        name: "Trans. From",
        fieldName: "trans_from",
        data: "string",
        ariaLabel:
          "Column operations for Trans From, Press to sort on Trans From",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      trans_to: {
        key: "trans_to",
        name: "Trans. To",
        fieldName: "trans_to",
        data: "string",
        ariaLabel: "Column operations for Trans To, Press to sort on Trans To",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      geocode: {
        key: "geocode",
        name: "Geocode",
        fieldName: "geocode",
        data: "number",
        ariaLabel: "Column operations for Geocode, Press to sort on Geocode",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted Lowest to Highest",
        sortDescendingLabel: "Sorted Highest to Lowest",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
    };

    const filteredColumns = this._filterColumns(columns, this._headers);

    const colFilters = this._headers.filter((e) => {
      if (e.filter) return e;
    });

    const selectedFilters = {
      filter1: { dropdown: colFilters[0], textField: "" },
      filter2: { dropdown: colFilters[1], textField: "" },
      filter3: { dropdown: colFilters[2], textField: "" },
    };

    this._selection = new Selection({
      onSelectionChanged: () => {
        this.setState({
          selectionDetails: this._getSelectionDetails(),
        });
      },
    });

    this.state = {
      offset: 0,
      // TODO Adjust default based on display size only on componentDidMount()
      limit: {
        key: 25,
        text: "25",
      },
      items: [],
      columns: columns,
      filteredColumns: filteredColumns,
      selectionDetails: this._getSelectionDetails(),
      isCompactMode: false,
      isToday: true,
      showControl: false,
      isFiltered: false,
      colFilters: colFilters,
      selectedFilters: selectedFilters,
      announcedMessage: undefined,
      report: this.props.report,
      height: 0,
      currentPage: 1,
      pageCount: 1,
    };
  }

  public render() {
    const {
      filteredColumns,
      isCompactMode,
      items,
      selectionDetails,
      isToday,
      showControl,
      colFilters,
      selectedFilters,
      announcedMessage,
    } = this.state;
    const filterIcon: IIconProps = { iconName: "FilterSettings" };
    const controlHeight = 250;

    const gridStyles: Partial<IDetailsListStyles> = {
      root: {
        height: "100%",
        overflowX: "scroll",
        selectors: {
          "& [role=grid]": {
            display: "flex",
            flexDirection: "column",
            alignItems: "start",
            height: "100%",
          },
        },
      },
      headerWrapper: {
        flex: "0 0 auto",
      },
      // TODO Create function to fix height modifier based on breakpoints
      contentWrapper: {
        flex: "1 1 auto",
        overflowY: "auto",
        overflowX: "hidden",
        height: showControl
          ? this.state.height * 0.6 - controlHeight
          : this.state.height * 0.6,
      },
    };

    return (
      <ThemeProvider>
        {showControl && (
          <div
            style={{ height: controlHeight }}
            className={`${styles.controlWrapper} ${
              showControl ? "ms-slideDownIn20" : "ms-slideDownOut"
            } ms-Grid`}
          >
            <div className={`${styles.controlRow} ms-Grid-row`}>
              <div className={`ms-Grid-col ms-sm4 ms-md4 ms-lg-2`}>
                <Dropdown
                  className={styles.control}
                  label="Items to display"
                  selectedKey={this.state.limit.key}
                  options={this._limitChoices}
                  onChange={(e, item) => this._onSelectLimit(item)}
                />
              </div>
              <div className={`ms-Grid-col ms-sm4 ms-md4 ms-lg-2`}>
                <Toggle
                  label="Enable compact mode"
                  checked={isCompactMode}
                  onChange={this._onChangeCompactMode}
                  onText="Compact"
                  offText="Normal"
                  className={styles.control}
                />
              </div>
              <div className={`ms-Grid-col ms-sm4 ms-md4 ms-lg-8`}>
                <Toggle
                  label="Change report range"
                  checked={isToday}
                  onChange={this._onChangeViewToday}
                  onText="Today"
                  offText="All"
                  className={styles.control}
                />
              </div>
            </div>
            <div className={`${styles.controlRow} ms-Grid-row`}>
              <div className={`ms-Grid-col ms-md4 ms-lg-8`}>
                <Dropdown
                  className={styles.control}
                  label="Filter by"
                  placeholder="Select column..."
                  selectedKey={selectedFilters["filter1"].dropdown.key}
                  options={colFilters}
                  onChange={(e, item) => this._onSelectFilter("filter1", item)}
                />
                <TextField
                  onChange={(ev, text) =>
                    this._onChangeText(ev, text, "filter1")
                  }
                  value={selectedFilters["filter1"].textField}
                  className={styles.control}
                />
                <Announced
                  message={`Number of items after filter applied: ${items.length}.`}
                />
              </div>
              <div className={`ms-Grid-col ms-md4 ms-lg-8`}>
                <Dropdown
                  className={styles.control}
                  label="Filter by"
                  placeholder="Select column..."
                  selectedKey={selectedFilters["filter2"].dropdown.key}
                  options={colFilters}
                  onChange={(e, item) => this._onSelectFilter("filter2", item)}
                />
                <TextField
                  onChange={(ev, text) =>
                    this._onChangeText(ev, text, "filter2")
                  }
                  className={styles.control}
                />
                <Announced
                  message={`Number of items after filter applied: ${items.length}.`}
                />
              </div>
              <div className={`ms-Grid-col ms-md4 ms-lg-8`}>
                <Dropdown
                  className={styles.control}
                  label="Filter by"
                  placeholder="Select column..."
                  selectedKey={selectedFilters["filter3"].dropdown.key}
                  options={colFilters}
                  onChange={(e, item) => this._onSelectFilter("filter3", item)}
                />
                <TextField
                  onChange={(ev, text) =>
                    this._onChangeText(ev, text, "filter3")
                  }
                  className={styles.control}
                />
                <Announced
                  message={`Number of items after filter applied: ${items.length}.`}
                />
              </div>
            </div>
            <div className={`${styles.controlRow} ms-Grid-row`} dir="rtl">
              <div className={`ms-Grid-col ms-sm12`}>
                <PrimaryButton
                  text="Apply Filters"
                  onClick={() => this._onApplyFilters()}
                />
              </div>
            </div>
          </div>
        )}
        <div className={styles.selectionDetails}>{selectionDetails}</div>
        <Announced message={selectionDetails} />
        {announcedMessage ? (
          <Announced message={announcedMessage} />
        ) : undefined}
        <div className={`ms-Grid-row`} dir="rtl">
          <div className={`ms-Grid-col ms-sm12`}>
            <IconButton
              className={styles.filterIcon}
              iconProps={filterIcon}
              onClick={this._onClickFilter}
              title="Filter"
              ariaLabel="Filter"
            ></IconButton>
          </div>
        </div>
        <div className={`ms-Grid-row`}>
          <div className={`${styles.detailsList} ms-Grid-col ms-sm12`}>
            <DetailsList
              items={items}
              compact={isCompactMode}
              columns={filteredColumns}
              selectionMode={SelectionMode.none}
              getKey={this._getId}
              setKey="none"
              styles={gridStyles}
              layoutMode={DetailsListLayoutMode.justified}
              isHeaderVisible={true}
              onItemInvoked={this._onItemInvoked}
              onRenderDetailsHeader={this.onRenderDetailsHeader}
            />
          </div>
        </div>
        <div className={`ms-Grid-row ${styles.pagination}`} dir="ltr">
          <div className={`ms-Grid-col ms-sm12`}>
            <Pagination
              currentPage={this.state.currentPage}
              totalPages={this.state.pageCount}
              hideFirstAndLastPageLinks={true}
              onChange={(page) => {
                this._onChangePage(page);
              }}
            />
          </div>
        </div>
      </ThemeProvider>
    );
  }

  public componentDidMount() {
    this._updateWindowDimensions();
    window.addEventListener("resize", this._updateWindowDimensions);

    this._getItems();
  }

  public componentWillUnmount() {
    window.removeEventListener("resize", this._updateWindowDimensions);
  }

  private _updateWindowDimensions() {
    this.setState({ height: window.innerHeight });
  }

  private _getItems(additionalParams?: string) {
    // Make API call for today and all report data (only page 1)
    let paginationParams: string = `p/${
      this.state.isToday ? "today/" : ""
    }?limit=${this.state.limit.key}&offset=${this.state.offset}/`;

    let req: string = this._apiURL.concat(paginationParams);

    axios.get(req).then((res) => {
      console.log(res);
      const resItems = res.data;
      this._items = resItems.results;

      const pageCount = Math.ceil(
        resItems.count / parseInt(this.state.limit.text)
      );

      this.setState({
        items: this._items,
        pageCount: pageCount,
      });
    });
  }

  private _getId(item: any, index?: number): string {
    return item.id;
  }

  private _onSelectLimit = (selected: IDropdownOption): void => {
    if (this.state.limit.key !== selected.key && !this.state.isFiltered) {
      this.setState(
        {
          items: [],
          offset: 0,
          limit: selected,
          currentPage: 1,
        },
        () => this._getItems()
      );
    } else if (this.state.isFiltered) {
      this.setState(
        {
          items: [],
          limit: selected,
        },
        () => this._onChangePage(1)
      );
    }
  };

  private _onChangeCompactMode = (
    ev: React.MouseEvent<HTMLElement>,
    checked: boolean
  ): void => {
    this.setState({ isCompactMode: checked });
  };

  private _onClickFilter = (): void => {
    this.setState({ showControl: !this.state.showControl });
  };

  private _onChangeViewToday = (
    ev: React.MouseEvent<HTMLElement>,
    checked: boolean
  ): void => {
    this.setState(
      {
        items: [],
        offset: 0,
        isToday: checked,
        currentPage: 1,
      },
      () => this._getItems()
    );
  };

  private _onChangeText = (
    ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>,
    text: string,
    currFilter: string
  ): void => {
    let selected = this.state.selectedFilters;

    selected[currFilter].textField = text;
    this.setState({ selectedFilters: selected });
  };

  // TODO FIX THIS IT NEEDS TO BE DONE ON THE BACK END
  private _onApplyFilters() {
    this.setState({
      items: [],
      isFiltered: true,
    });

    // Make API call for today and all report data (all, unpaginated)
    let urlParams: string = `${this.state.isToday ? "today/" : ""}`;
    let req: string = this._apiURL.concat(urlParams);

    let selected = this.state.selectedFilters;

    const filtText1 = selected["filter1"].textField.toLowerCase();
    const filtText2 = selected["filter2"].textField.toLowerCase();
    const filtText3 = selected["filter3"].textField.toLowerCase();

    axios.get(req).then((res) => {
      this._items = res.data;

      const allItemsCopy = this._items.filter((i) => {
        return (
          i[selected["filter1"].dropdown.key]
            .toString()
            .toLowerCase()
            .indexOf(filtText1) > -1 &&
          i[selected["filter2"].dropdown.key]
            .toString()
            .toLowerCase()
            .indexOf(filtText2) > -1 &&
          i[selected["filter3"].dropdown.key]
            .toString()
            .toLowerCase()
            .indexOf(filtText3) > -1
        );
      });

      this._items = allItemsCopy;

      const pageCount = Math.ceil(
        this._items.length / parseInt(this.state.limit.text)
      );

      this.setState(
        {
          pageCount: pageCount,
        },
        () => this._onChangePage(1)
      );
    });
  }

  private _onItemInvoked(item: any): void {
    alert(`Item invoked: ${item.name}`);
  }

  private _getSelectionDetails(): string {
    const selectionCount = this._selection.getSelectedCount();

    switch (selectionCount) {
      case 0:
        return "No items selected";
      case 1:
        return (
          "1 item selected: " +
          (this._selection.getSelection()[0] as IItem).lic_num
        );
      default:
        return `${selectionCount} items selected`;
    }
  }

  private _onColumnClick = (
    ev: React.MouseEvent<HTMLElement>,
    column: IColumn
  ): void => {
    const { filteredColumns, items } = this.state;
    const newColumns: IColumn[] = filteredColumns.slice();
    const currColumn: IColumn = newColumns.filter(
      (currCol) => column.key === currCol.key
    )[0];
    newColumns.forEach((newCol: IColumn) => {
      if (newCol === currColumn) {
        currColumn.isSortedDescending = !currColumn.isSortedDescending;
        currColumn.isSorted = true;
        this.setState({
          announcedMessage: `${currColumn.name} is sorted ${
            currColumn.isSortedDescending ? "descending" : "ascending"
          }`,
        });
      } else {
        newCol.isSorted = false;
        newCol.isSortedDescending = true;
      }
    });
    const newItems = _copyAndSort(
      items,
      currColumn.fieldName!,
      currColumn.isSortedDescending
    );
    this.setState({
      columns: newColumns,
      items: newItems,
    });
  };

  private _filterColumns(columns: Object, headers: Array<Header>): IColumn[] {
    let filtered: IColumn[] = [];
    headers.map((header) => {
      let key = header.key;
      filtered.push(columns[key]);
    });
    return filtered;
  }

  private _onSelectFilter = (filterNum: string, colFilter: any): void => {
    let selectedFiltersCopy = this.state.selectedFilters;
    selectedFiltersCopy[filterNum].dropdown = colFilter;

    this.setState({ selectedFilters: selectedFiltersCopy });
  };

  private onRenderDetailsHeader: IRenderFunction<IDetailsHeaderProps> = (
    props,
    defaultRender
  ) => {
    if (!props) {
      return null;
    }
    const onRenderColumnHeaderTooltip: IRenderFunction<IDetailsColumnRenderTooltipProps> =
      (tooltipHostProps) => <TooltipHost {...tooltipHostProps} />;
    return defaultRender!({
      ...props,
      onRenderColumnHeaderTooltip,
    });
  };

  private _onChangePage(page: number) {
    if (page !== this.state.currentPage && !this.state.isFiltered) {
      const newOffset = (page - 1) * parseInt(this.state.limit.text);

      this.setState(
        {
          items: [],
          currentPage: page,
          offset: newOffset,
        },
        () => this._getItems()
      );
    } else if (this.state.isFiltered) {
      const newOffset = (page - 1) * parseInt(this.state.limit.text);
      const { limit } = this.state;
      const start = newOffset;
      let end;

      if (newOffset + parseInt(limit.text) < this._items.length) {
        end = newOffset + parseInt(limit.text);
      } else {
        end = this._items.length;
      }

      const paginatedItems = this._items.slice(start, end);

      this.setState({
        items: paginatedItems,
        currentPage: page,
        offset: newOffset,
      });
    }
  }
}

function _copyAndSort<T>(
  items: T[],
  columnKey: string,
  isSortedDescending?: boolean
): T[] {
  const key = columnKey as keyof T;
  return items
    .slice(0)
    .sort((a: T, b: T) =>
      (isSortedDescending ? a[key] < b[key] : a[key] > b[key]) ? 1 : -1
    );
}
