import React from "react";
import { DocumentPage } from "../types";

interface PageOrderListProps {
  pages: DocumentPage[];
}

export function PageOrderList({ pages }: PageOrderListProps) {
  return (
    <ol>
      {pages.map((page) => (
        <li key={page.pageId}>
          Page {page.pageNumber}: {page.fileName}
        </li>
      ))}
    </ol>
  );
}
