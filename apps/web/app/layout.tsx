import "./globals.css";

import { ReactNode } from "react";

import { AppFooter } from "@/components/layout/footer";
import { AppNav } from "@/components/layout/nav";

export const metadata = {
  title: {
    template: "%s · Student Digital Twin",
    default: "Student Digital Twin"
  },
  description:
    "Teacher-oriented early-warning analytics for student cohorts, powered by explainable AI."
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppNav />
        {children}
        <AppFooter />
      </body>
    </html>
  );
}
