import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export function IdentityChip() {
  return (
    <div className="flex items-center gap-2" aria-label="Signed in teacher">
      <Avatar className="h-8 w-8">
        <AvatarFallback>MC</AvatarFallback>
      </Avatar>
      <span className="flex flex-col leading-tight">
        <span className="text-sm font-medium">Ms. Carter</span>
        <span className="text-xs text-muted-foreground">DDD 2013J</span>
      </span>
    </div>
  );
}
