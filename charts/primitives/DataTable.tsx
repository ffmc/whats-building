import { useId, useState } from "react";

export type Column<T> = {
  key: keyof T & string;
  label: string;
  format?: (value: T[keyof T]) => string;
};

type Props<T> = {
  rows: T[];
  columns: Column<T>[];
  caption: string;
};

export function DataTable<T extends Record<string, unknown>>({
  rows,
  columns,
  caption,
}: Props<T>) {
  const [open, setOpen] = useState(false);
  const id = useId();

  return (
    <div className="chart-table">
      <button type="button" onClick={() => setOpen(!open)} aria-expanded={open} aria-controls={id}>
        {open ? "Hide data table" : "Show data table"}
      </button>
      <table id={id} hidden={!open}>
        <caption>{caption}</caption>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key} scope="col">
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column.key}>
                  {column.format ? column.format(row[column.key]) : String(row[column.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
