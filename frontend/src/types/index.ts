export type UserCredentials = {
  username: string;
  password: string;
};

export type RegisterCredentials = {
  username: string;
  email: string;
  password: string;
};

export type FileUploadData = {
  docxFile: File | null;
  xlsxFile: File | null;
};