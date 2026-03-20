import { apiClient } from "../../../api/client";
import { API_ROUTES } from "../../../api/routes";
import {
  BusinessRegistrationInput,
  LoginInput,
  PersonalRegistrationInput
} from "../types";

export async function registerPersonal(payload: PersonalRegistrationInput) {
  return apiClient(`${API_ROUTES.identityAdmin}/register/personal`, {
    method: "POST",
    body: payload
  });
}

export async function registerBusiness(payload: BusinessRegistrationInput) {
  return apiClient(`${API_ROUTES.identityAdmin}/register/business`, {
    method: "POST",
    body: payload
  });
}

export async function login(payload: LoginInput) {
  return apiClient(`${API_ROUTES.identityAdmin}/login`, {
    method: "POST",
    body: payload
  });
}

export async function logout() {
  return apiClient(`${API_ROUTES.identityAdmin}/logout`, {
    method: "POST"
  });
}

export async function getUsers() {
  return apiClient(`${API_ROUTES.identityAdmin}/users`, {
    method: "GET"
  });
}

export async function getRoles() {
  return apiClient(`${API_ROUTES.identityAdmin}/roles`, {
    method: "GET"
  });
}

export async function getMandates() {
  return apiClient(`${API_ROUTES.identityAdmin}/mandates`, {
    method: "GET"
  });
}
