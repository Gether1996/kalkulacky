// Blog Models

export interface BlogCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  color: string;
  icon: string;
  order: number;
  post_count: number;
  created_at: string;
}

export interface BlogPostSummary {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  featured_image_url: string;
  category_name: string;
  category_slug: string;
  category_color: string;
  tags_list: string[];
  published_at: string;
  view_count: number;
  read_time: string;
  related_calculator: string;
}

export interface BlogPostDetail {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  content_html: string;
  meta_keywords: string;
  featured_image_url: string;
  category: BlogCategory;
  tags_list: string[];
  related_calculator: string;
  status: string;
  published_at: string;
  view_count: number;
  read_time: string;
  related_posts: BlogPostSummary[];
  created_at: string;
  updated_at: string;
}

export interface BlogListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: BlogPostSummary[];
}
