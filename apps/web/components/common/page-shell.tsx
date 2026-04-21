import { ReactNode } from "react";

type Props = { title: string; children?: ReactNode };

export function PageShell({ title, children }: Props) {
  return (
    <main style={{ padding: 20 }}>
      <h1>{title}</h1>
      {children}
    </main>
  );
}
