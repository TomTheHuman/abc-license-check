export interface Page {
  name: string;
  formalName: string;
}

export interface IAbcLicCheckState {
  currentPage: Page;
  repMenuOpen: boolean;
  optMenuOpen: boolean;
  options: Array<any>;
  pages: Array<any>;
}