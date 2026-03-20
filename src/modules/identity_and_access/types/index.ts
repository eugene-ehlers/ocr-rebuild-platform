export type JourneyType = "personal" | "business";

export interface PersonalRegistrationInput {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

export interface BusinessRegistrationInput {
  businessName: string;
  registrationNumber: string;
  adminFirstName: string;
  adminLastName: string;
  email: string;
  password: string;
}

export interface LoginInput {
  email: string;
  password: string;
}

export interface IdentityUser {
  userId: string;
  journeyType: JourneyType;
  email: string;
  roles: string[];
  mandates: string[];
  status: "active" | "inactive" | "pending";
}
