/**
 * Shared Type Definitions for EcoSort AI (RC-1 Release Candidate)
 */

export enum UserRole {
  CITIZEN = 'CITIZEN',
  BWG = 'BWG', // Bulk Waste Generator (School / College / Institution)
  VENDOR = 'VENDOR', // Scrap Vendor / Kabadiwala / Recycling Partner
  MUNICIPALITY = 'MUNICIPALITY', // Municipal Officer / Sanitary Inspector
  ADMIN = 'ADMIN' // Super Admin
}

export enum WasteCategory {
  DRY_RECYCLABLE = 'DRY_RECYCLABLE',
  WET_ORGANIC = 'WET_ORGANIC',
  HAZARDOUS = 'HAZARDOUS',
  E_WASTE = 'E_WASTE',
  TEXTILE = 'TEXTILE',
  CONSTRUCTION = 'CONSTRUCTION'
}

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  role: UserRole;
  preferred_language: 'en' | 'hi';
  rewards_balance: number;
  sustainability_score: number;
  carbon_saved_kg: number;
  badges: string[];
  is_active: boolean;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthResponse {
  tokens: AuthTokens;
  user: UserProfile;
}

export interface APIResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  error?: {
    code: string;
    details: string;
  };
}

export interface ScanResult {
  id: string;
  user_id: string;
  image_url: string;
  primary_label: string;
  waste_category: WasteCategory;
  confidence_score: number;
  bin_color: 'BLUE' | 'GREEN' | 'RED' | 'BLACK' | 'YELLOW';
  urban_instructions: string;
  rural_instructions: string;
  upcycling_ideas: string[];
  eco_coins_earned: number;
  carbon_saved_kg: number;
  created_at: string;
}

export interface BadgeInfo {
  id: string;
  code: string;
  title: string;
  description: string;
  icon: string;
  unlocked: boolean;
  unlocked_at?: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  type: 'INFO' | 'REWARD' | 'PICKUP' | 'SYSTEM';
  is_read: boolean;
  created_at: string;
}

export interface RecyclingCenter {
  id: string;
  name: string;
  type: 'KABADIWALA_PARTNER' | 'E_WASTE_KIOSK' | 'MUNICIPAL_DUMP';
  contact_phone: string;
  address: string;
  city: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  accepted_categories: WasteCategory[];
  qr_code_data: string;
  is_verified: boolean;
}

export interface PickupRequest {
  id: string;
  citizen_id: string;
  vendor_id?: string;
  waste_categories: WasteCategory[];
  estimated_weight_kg: number;
  pickup_date: string;
  address: string;
  status: 'SCHEDULED' | 'COMPLETED' | 'CANCELLED';
  created_at: string;
}

export interface WardWasteStats {
  ward_id: string;
  ward_name: string;
  total_scans: number;
  dry_waste_kg: number;
  wet_waste_kg: number;
  hazardous_kg: number;
  carbon_reduction_kg: number;
}

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  full_name: string;
  sustainability_score: number;
  carbon_saved_kg: number;
  badges_count: number;
}
