interface RouteGuardInput {
  isAuthenticated: boolean;
  requiredRole?: string;
  userRoles?: string[];
}

export function useRouteGuard() {
  function canAccess(input: RouteGuardInput) {
    const hasRole =
      !input.requiredRole ||
      Boolean(input.userRoles?.includes(input.requiredRole));

    return {
      success: true,
      status: "placeholder",
      message: "Route guard scaffold created.",
      data: {
        allowed: input.isAuthenticated && hasRole,
        reason: input.isAuthenticated ? (hasRole ? "allowed" : "missing_role") : "not_authenticated"
      }
    };
  }

  return { canAccess };
}
