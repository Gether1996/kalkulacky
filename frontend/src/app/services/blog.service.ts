import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { 
  BlogCategory, 
  BlogPostSummary, 
  BlogPostDetail, 
  BlogListResponse 
} from '../models/blog.models';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BlogService {
  private apiUrl: string;
  private platformId = inject(PLATFORM_ID);

  constructor(private http: HttpClient) {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? `${environment.apiUrl}/calculators`
      : 'http://backend:8000/api/calculators';
  }

  // Get all blog categories
  getCategories(): Observable<BlogCategory[]> {
    return this.http.get<BlogCategory[]>(`${this.apiUrl}/blog/categories/`);
  }

  // Get all blog posts (with optional filters)
  getPosts(params?: {
    category?: string;
    calculator?: string;
    tag?: string;
    search?: string;
  }): Observable<BlogPostSummary[]> {
    let url = `${this.apiUrl}/blog/posts/`;
    const queryParams: string[] = [];
    
    if (params) {
      if (params.category) queryParams.push(`category=${params.category}`);
      if (params.calculator) queryParams.push(`calculator=${params.calculator}`);
      if (params.tag) queryParams.push(`tag=${params.tag}`);
      if (params.search) queryParams.push(`search=${params.search}`);
    }
    
    if (queryParams.length > 0) {
      url += '?' + queryParams.join('&');
    }
    
    return this.http.get<BlogPostSummary[]>(url);
  }

  // Get single blog post by slug
  getPost(slug: string): Observable<BlogPostDetail> {
    return this.http.get<{ success: boolean; data: BlogPostDetail }>(
      `${this.apiUrl}/blog/posts/${slug}/`
    ).pipe(map(response => response.data));
  }

  // Get featured/latest blog posts
  getFeaturedPosts(): Observable<BlogPostSummary[]> {
    return this.http.get<BlogPostSummary[]>(`${this.apiUrl}/blog/featured/`);
  }
}
