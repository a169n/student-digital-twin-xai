import "./globals.css";

import { ReactNode } from "react";

import { AppFooter } from "@/components/layout/footer";
import { AppNav } from "@/components/layout/nav";

export const metadata = {
  title: "Student Digital Twin XAI",
  description: "Teacher-oriented research prototype UI",
  icons: {
    icon: "/icon.svg"
  }
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
